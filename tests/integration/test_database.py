#!/usr/bin/env python3
"""
Integration tests for database operations
"""

import pytest
import psycopg2
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the scripts directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../scripts'))

from migrate_excel_data import ExcelDataMigrator

class TestDatabaseConnection:
    """Test database connectivity and basic operations"""
    
    def test_database_connection(self):
        """Test that we can connect to the database"""
        migrator = ExcelDataMigrator("dummy_path")
        assert migrator.connect_db() == True
        migrator.connection.close()
    
    def test_database_tables_exist(self):
        """Test that all required tables exist"""
        migrator = ExcelDataMigrator("dummy_path")
        migrator.connect_db()
        
        cursor = migrator.connection.cursor()
        
        # Check for required tables
        required_tables = [
            'products', 'categories', 'brands', 'inventory',
            'sales', 'orders', 'order_items', 'platform_goals',
            'admin_costs', 'users'
        ]
        
        for table in required_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table,))
            exists = cursor.fetchone()[0]
            assert exists == True, f"Table {table} does not exist"
        
        cursor.close()
        migrator.connection.close()
    
    def test_database_schema_integrity(self):
        """Test database schema integrity"""
        migrator = ExcelDataMigrator("dummy_path")
        migrator.connect_db()
        
        cursor = migrator.connection.cursor()
        
        # Test products table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'products'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        expected_columns = [
            ('id', 'uuid'),
            ('item_inventory_number', 'character varying'),
            ('name', 'character varying'),
            ('description', 'text'),
            ('category_id', 'uuid'),
            ('brand_id', 'uuid'),
            ('created_at', 'timestamp with time zone'),
            ('updated_at', 'timestamp with time zone')
        ]
        
        for i, (col_name, data_type) in enumerate(columns):
            assert i < len(expected_columns)
            expected_name, expected_type = expected_columns[i]
            assert col_name == expected_name, f"Column {col_name} not found"
            # Note: data_type might vary slightly, so we check if it contains the expected type
            assert expected_type in data_type, f"Column {col_name} has wrong type: {data_type}"
        
        cursor.close()
        migrator.connection.close()

class TestDatabaseOperations:
    """Test database CRUD operations"""
    
    def test_insert_and_select_product(self):
        """Test inserting and selecting a product"""
        migrator = ExcelDataMigrator("dummy_path")
        migrator.connect_db()
        
        cursor = migrator.connection.cursor()
        
        # Insert a test product
        test_product = {
            'item_inventory_number': 'TEST001',
            'name': 'Test Product',
            'description': 'A test product for integration testing'
        }
        
        cursor.execute("""
            INSERT INTO products (item_inventory_number, name, description)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (test_product['item_inventory_number'], test_product['name'], test_product['description']))
        
        product_id = cursor.fetchone()[0]
        assert product_id is not None
        
        # Select the product
        cursor.execute("""
            SELECT item_inventory_number, name, description
            FROM products
            WHERE id = %s;
        """, (product_id,))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == test_product['item_inventory_number']
        assert result[1] == test_product['name']
        assert result[2] == test_product['description']
        
        # Clean up
        cursor.execute("DELETE FROM products WHERE id = %s;", (product_id,))
        migrator.connection.commit()
        
        cursor.close()
        migrator.connection.close()
    
    def test_foreign_key_constraints(self):
        """Test foreign key constraints"""
        migrator = ExcelDataMigrator("dummy_path")
        migrator.connect_db()
        
        cursor = migrator.connection.cursor()
        
        # Try to insert inventory with non-existent product_id
        try:
            cursor.execute("""
                INSERT INTO inventory (product_id, quantity)
                VALUES ('00000000-0000-0000-0000-000000000000', 10);
            """)
            # This should fail due to foreign key constraint
            assert False, "Should have failed due to foreign key constraint"
        except psycopg2.IntegrityError:
            # Expected behavior
            pass
        
        migrator.connection.rollback()
        cursor.close()
        migrator.connection.close()

class TestMigrationScripts:
    """Test migration script functionality"""
    
    def test_migrator_initialization(self):
        """Test that the migrator can be initialized"""
        migrator = ExcelDataMigrator("dummy_path")
        assert migrator.excel_file_path == "dummy_path"
        assert migrator.connection is None
    
    def test_database_config_parsing(self):
        """Test database configuration parsing"""
        migrator = ExcelDataMigrator("dummy_path")
        config = migrator._get_db_config()
        
        # Check that all required keys are present
        required_keys = ['host', 'database', 'user', 'password', 'port']
        for key in required_keys:
            assert key in config
        
        # Check that port is an integer
        assert isinstance(config['port'], int)
    
    def test_environment_variable_usage(self):
        """Test that environment variables are used correctly"""
        # Set test environment variables
        os.environ['POSTGRES_DB'] = 'test_db'
        os.environ['POSTGRES_USER'] = 'test_user'
        os.environ['POSTGRES_PASSWORD'] = 'test_password'
        
        migrator = ExcelDataMigrator("dummy_path")
        config = migrator._get_db_config()
        
        assert config['database'] == 'test_db'
        assert config['user'] == 'test_user'
        assert config['password'] == 'test_password'
        
        # Clean up
        del os.environ['POSTGRES_DB']
        del os.environ['POSTGRES_USER']
        del os.environ['POSTGRES_PASSWORD']

class TestDatabasePerformance:
    """Test database performance characteristics"""
    
    def test_index_usage(self):
        """Test that indexes are being used"""
        migrator = ExcelDataMigrator("dummy_path")
        migrator.connect_db()
        
        cursor = migrator.connection.cursor()
        
        # Check if indexes exist
        cursor.execute("""
            SELECT indexname, tablename
            FROM pg_indexes
            WHERE tablename IN ('products', 'inventory', 'sales')
            ORDER BY tablename, indexname;
        """)
        
        indexes = cursor.fetchall()
        assert len(indexes) > 0, "No indexes found on main tables"
        
        # Check for specific important indexes
        index_names = [idx[0] for idx in indexes]
        expected_indexes = [
            'idx_products_item_inventory_number',
            'idx_inventory_product_id',
            'idx_sales_product_id'
        ]
        
        for expected_index in expected_indexes:
            assert expected_index in index_names, f"Index {expected_index} not found"
        
        cursor.close()
        migrator.connection.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 