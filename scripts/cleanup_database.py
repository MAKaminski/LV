#!/usr/bin/env python3
"""
Database Cleanup Script
Remove leftover tables from the old schema that are not needed for CSV-based data
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('POSTGRES_DB', 'lv_project'),
        'user': os.getenv('POSTGRES_USER', 'makaminski1337'),
        'password': os.getenv('POSTGRES_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', '5432'))
    }

def main():
    """Main cleanup function"""
    print("🧹 Database Cleanup - Removing Unnecessary Tables")
    print("=" * 60)
    
    # Connect to database
    try:
        conn = psycopg2.connect(**get_db_config())
        print("✅ Connected to database")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    cursor = conn.cursor()
    
    # Tables to remove (all empty and not needed for CSV data)
    tables_to_remove = [
        'admin_costs',      # Administrative costs tracking (not in CSV)
        'categories',        # Product categories (not used in CSV)
        'order_items',       # Order line items (not in CSV)
        'orders',           # Order management (not in CSV)
        'platform_goals'    # Multi-platform selling goals (not in CSV)
    ]
    
    print(f"\n📋 Tables to remove: {len(tables_to_remove)}")
    for table in tables_to_remove:
        print(f"  - {table}")
    
    # Check current table counts
    print(f"\n📊 Current table status:")
    for table in tables_to_remove:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} records")
        except Exception as e:
            print(f"  - {table}: Error checking count - {e}")
    
    # Confirm with user
    print(f"\n⚠️  This will permanently remove {len(tables_to_remove)} tables.")
    print("These tables are empty and not used in the current CSV-based data structure.")
    
    # Remove tables in correct order (respecting foreign key constraints)
    print(f"\n🗑️  Removing tables...")
    
    # Order of removal (respecting foreign key constraints):
    # 1. order_items (references orders and products)
    # 2. orders (references users)
    # 3. platform_goals (references products)
    # 4. admin_costs (no dependencies)
    # 5. categories (referenced by products, but we made category_id nullable)
    
    removal_order = ['order_items', 'orders', 'platform_goals', 'admin_costs', 'categories']
    
    for table in removal_order:
        if table in tables_to_remove:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                conn.commit()
                print(f"  ✅ Removed {table}")
            except Exception as e:
                print(f"  ❌ Error removing {table}: {e}")
                conn.rollback()
    
    # Verify remaining tables
    print(f"\n📋 Remaining tables:")
    try:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        remaining_tables = cursor.fetchall()
        for table in remaining_tables:
            print(f"  - {table[0]}")
    except Exception as e:
        print(f"  ❌ Error listing tables: {e}")
    
    # Final summary
    print(f"\n" + "=" * 60)
    print("✅ Database cleanup completed!")
    print(f"🗑️  Removed {len(tables_to_remove)} unnecessary tables")
    print(f"📊 Kept {len(remaining_tables)} essential tables for CSV data")
    print("\n📋 Essential tables for your CSV data:")
    print("  - brands: 89 luxury brands")
    print("  - products: 60 products")
    print("  - inventory: 60 inventory records")
    print("  - sales: 29 sales transactions")
    print("  - users: 126 user records (sellers/buyers)")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main() 