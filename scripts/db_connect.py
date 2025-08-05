#!/usr/bin/env python3
"""
Database Connection Script for LV Project
Quick way to connect and explore the database
"""

import psycopg2
import pandas as pd
from tabulate import tabulate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseExplorer:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to the LV Project database"""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="lv_project",
                user="makaminski1337",
                password="",
                port="5432"
            )
            print("✅ Connected to LV Project Database")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    def get_table_info(self):
        """Get information about all tables"""
        query = """
        SELECT 
            table_name,
            (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as columns
        FROM information_schema.tables t
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        
        df = pd.read_sql_query(query, self.connection)
        print("\n📊 Database Tables:")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    def get_data_summary(self):
        """Get summary of data in each table"""
        tables = ['products', 'inventory', 'sales', 'categories', 'brands']
        
        print("\n📈 Data Summary:")
        for table in tables:
            try:
                count_query = f"SELECT COUNT(*) as count FROM {table}"
                df = pd.read_sql_query(count_query, self.connection)
                count = df['count'].iloc[0]
                print(f"  {table.capitalize()}: {count} records")
            except Exception as e:
                print(f"  {table.capitalize()}: Error - {e}")
    
    def show_sample_data(self, table_name, limit=5):
        """Show sample data from a table"""
        try:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            df = pd.read_sql_query(query, self.connection)
            print(f"\n📋 Sample data from {table_name}:")
            print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        except Exception as e:
            print(f"❌ Error showing {table_name}: {e}")
    
    def run_query(self, query):
        """Run a custom SQL query"""
        try:
            df = pd.read_sql_query(query, self.connection)
            print(f"\n🔍 Query Results:")
            print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        except Exception as e:
            print(f"❌ Query error: {e}")
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

def main():
    """Main function to explore the database"""
    explorer = DatabaseExplorer()
    
    if not explorer.connection:
        return
    
    print("\n" + "="*50)
    print("🔍 LV PROJECT DATABASE EXPLORER")
    print("="*50)
    
    # Show table information
    explorer.get_table_info()
    
    # Show data summary
    explorer.get_data_summary()
    
    # Show sample data from key tables
    explorer.show_sample_data('products', 3)
    explorer.show_sample_data('sales', 3)
    explorer.show_sample_data('categories', 3)
    
    # Example queries
    print("\n" + "="*50)
    print("💡 EXAMPLE QUERIES")
    print("="*50)
    
    # Top products by inventory value
    explorer.run_query("""
        SELECT 
            p.name,
            p.item_inventory_number,
            i.quantity,
            i.purchase_price,
            (i.quantity * i.purchase_price) as total_value
        FROM products p
        JOIN inventory i ON p.id = i.product_id
        WHERE i.quantity > 0
        ORDER BY total_value DESC
        LIMIT 5
    """)
    
    # Sales analysis
    explorer.run_query("""
        SELECT 
            p.name,
            s.sell_price,
            s.net_profit_loss,
            s.percent_profit,
            s.date_sold
        FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.date_sold DESC
    """)
    
    explorer.close()

if __name__ == "__main__":
    main() 