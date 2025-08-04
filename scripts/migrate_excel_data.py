#!/usr/bin/env python3
"""
Script to migrate Excel data to PostgreSQL database
Feature 1: ERD + Schema Development
"""

import pandas as pd
import psycopg2
import os
import json
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ExcelDataMigrator:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.db_config = self._get_db_config()
        self.connection = None

    def _get_db_config(self):
        """Get database configuration from environment variables"""
        # Parse DATABASE_URL if available
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Simple parsing of DATABASE_URL
            # Format: postgresql://user:password@host:port/database
            if database_url.startswith("postgresql://"):
                parts = database_url.replace("postgresql://", "").split("@")
                if len(parts) == 2:
                    user_pass = parts[0].split(":")
                    host_db = parts[1].split("/")
                    if len(user_pass) >= 2 and len(host_db) >= 2:
                        host_port = host_db[0].split(":")
                        return {
                            'host': host_port[0],
                            'database': host_db[1],
                            'user': user_pass[0],
                            'password': user_pass[1],
                            'port': int(host_port[1]) if len(host_port) > 1 else 5432
                        }
        
        # Fallback to individual environment variables
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('POSTGRES_DB', 'lv_project'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'your_secure_password'),
            'port': int(os.getenv('DB_PORT', '5432'))
        }

    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ Connected to PostgreSQL database")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

    def migrate_categories(self):
        """Migrate product categories from Excel"""
        print("\n📋 Migrating categories...")

        try:
            # Read the For Listing PM sheet to get categories
            df = pd.read_excel(self.excel_file_path, sheet_name='For Listing PM')

            # Extract unique categories
            categories = df['product category'].dropna().unique()

            cursor = self.connection.cursor()

            for category in categories:
                if category and str(category).strip():
                    # Check if category already exists
                    cursor.execute("SELECT id FROM categories WHERE name = %s", (str(category),))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO categories (name, description) VALUES (%s, %s)",
                            (str(category), f"Category for {str(category)}")
                        )
                        print(f"  ✅ Added category: {category}")

            self.connection.commit()
            cursor.close()
            print(f"✅ Migrated {len(categories)} categories")

        except Exception as e:
            print(f"❌ Error migrating categories: {str(e)}")

    def migrate_brands(self):
        """Migrate brands from Excel data"""
        print("\n🏷️  Migrating brands...")

        try:
            # Extract brands from product names and descriptions
            df_inventory = pd.read_excel(self.excel_file_path, sheet_name='Inventory')

            # Simple brand extraction (can be enhanced)
            brands = ['LaceLuxx', 'Generic', 'Vintage', 'Designer']

            cursor = self.connection.cursor()

            for brand in brands:
                cursor.execute("SELECT id FROM brands WHERE name = %s", (brand,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO brands (name, description) VALUES (%s, %s)",
                        (brand, f"Brand: {brand}")
                    )
                    print(f"  ✅ Added brand: {brand}")

            self.connection.commit()
            cursor.close()
            print(f"✅ Migrated {len(brands)} brands")

        except Exception as e:
            print(f"❌ Error migrating brands: {str(e)}")

    def migrate_products(self):
        """Migrate products from Excel"""
        print("\n📦 Migrating products...")

        try:
            # Read inventory sheet for products
            df_inventory = pd.read_excel(self.excel_file_path, sheet_name='Inventory')

            cursor = self.connection.cursor()

            # Get category and brand mappings
            cursor.execute("SELECT id, name FROM categories")
            categories = {row[1]: row[0] for row in cursor.fetchall()}

            cursor.execute("SELECT id, name FROM brands")
            brands = {row[1]: row[0] for row in cursor.fetchall()}

            products_migrated = 0

            for _, row in df_inventory.iterrows():
                try:
                    item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
                    product_name = str(row['product name']) if pd.notna(row['product name']) else 'Unknown Product'
                    description = str(row['product description']) if pd.notna(row['product description']) else None

                    if item_number and product_name:
                        # Determine category (simplified logic)
                        category_id = list(categories.values())[0] if categories else None
                        brand_id = list(brands.values())[0] if brands else None

                        # Check if product already exists
                        cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                        if not cursor.fetchone():
                            cursor.execute(
                                """INSERT INTO products
                                   (item_inventory_number, name, description, category_id, brand_id)
                                   VALUES (%s, %s, %s, %s, %s)""",
                                (item_number, product_name, description, category_id, brand_id)
                            )
                            products_migrated += 1

                except Exception as e:
                    print(f"  ⚠️  Error processing product {row.get('Item Inventory #', 'Unknown')}: {str(e)}")
                    continue

            self.connection.commit()
            cursor.close()
            print(f"✅ Migrated {products_migrated} products")

        except Exception as e:
            print(f"❌ Error migrating products: {str(e)}")

    def migrate_inventory(self):
        """Migrate inventory data"""
        print("\n📊 Migrating inventory...")

        try:
            df_inventory = pd.read_excel(self.excel_file_path, sheet_name='Inventory')

            cursor = self.connection.cursor()

            inventory_migrated = 0

            for _, row in df_inventory.iterrows():
                try:
                    item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None

                    if item_number:
                        # Get product ID
                        cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                        product_result = cursor.fetchone()

                        if product_result:
                            product_id = product_result[0]

                            # Extract inventory data
                            purchase_price = float(row['Purchase Price']) if pd.notna(row['Purchase Price']) else None
                            goal_earnings = float(row['Goal earnings']) if pd.notna(row['Goal earnings']) else None
                            floor_earnings = float(row['Floor Earnings']) if pd.notna(row['Floor Earnings']) else None
                            need_to_make = float(row['Need to Make']) if pd.notna(row['Need to Make']) else None
                            list_price = float(row['List Price']) if pd.notna(row['List Price']) else None
                            is_listed = bool(row['Listed?']) if pd.notna(row['Listed?']) else False
                            notes = str(row['Notes']) if pd.notna(row['Notes']) else None

                            # Check if inventory record exists
                            cursor.execute("SELECT id FROM inventory WHERE product_id = %s", (product_id,))
                            if not cursor.fetchone():
                                cursor.execute(
                                    """INSERT INTO inventory
                                       (product_id, purchase_price, goal_earnings, floor_earnings,
                                        need_to_make, list_price, is_listed, notes)
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                    (product_id, purchase_price, goal_earnings, floor_earnings,
                                     need_to_make, list_price, is_listed, notes)
                                )
                                inventory_migrated += 1

                except Exception as e:
                    print(f"  ⚠️  Error processing inventory for {row.get('Item Inventory #', 'Unknown')}: {str(e)}")
                    continue

            self.connection.commit()
            cursor.close()
            print(f"✅ Migrated {inventory_migrated} inventory records")

        except Exception as e:
            print(f"❌ Error migrating inventory: {str(e)}")

    def migrate_sales(self):
        """Migrate sales data"""
        print("\n💰 Migrating sales...")

        try:
            df_inventory = pd.read_excel(self.excel_file_path, sheet_name='Inventory')

            cursor = self.connection.cursor()

            sales_migrated = 0

            for _, row in df_inventory.iterrows():
                try:
                    item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
                    quantity_sold = int(row['Quantity Sold']) if pd.notna(row['Quantity Sold']) else 0
                    sell_price = float(row['Sell price']) if pd.notna(row['Sell price']) else None
                    gross_amount = float(row['Gross Amount Earned']) if pd.notna(row['Gross Amount Earned']) else None
                    net_profit = float(row['Net Profit/Loss']) if pd.notna(row['Net Profit/Loss']) else None
                    percent_profit = float(row['Percent Profit']) if pd.notna(row['Percent Profit']) else None
                    date_sold = row['Date Sold'] if pd.notna(row['Date Sold']) else None
                    days_held = int(row['Days Held']) if pd.notna(row['Days Held']) else None
                    comps = str(row['Comps']) if pd.notna(row['Comps']) else None
                    notes = str(row['Notes']) if pd.notna(row['Notes']) else None

                    if item_number and quantity_sold > 0 and sell_price:
                        # Get product ID
                        cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                        product_result = cursor.fetchone()

                        if product_result:
                            product_id = product_result[0]

                            cursor.execute(
                                """INSERT INTO sales
                                   (product_id, quantity_sold, sell_price, gross_amount_earned,
                                    net_profit_loss, percent_profit, date_sold, days_held, comps, notes)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (product_id, quantity_sold, sell_price, gross_amount, net_profit,
                                 percent_profit, date_sold, days_held, comps, notes)
                            )
                            sales_migrated += 1

                except Exception as e:
                    print(f"  ⚠️  Error processing sale for {row.get('Item Inventory #', 'Unknown')}: {str(e)}")
                    continue

            self.connection.commit()
            cursor.close()
            print(f"✅ Migrated {sales_migrated} sales records")

        except Exception as e:
            print(f"❌ Error migrating sales: {str(e)}")

    def run_migration(self):
        """Run the complete migration process"""
        print("🚀 Starting Excel to Database Migration")
        print("=" * 60)

        if not self.connect_db():
            return False

        try:
            # Run migrations in order
            self.migrate_categories()
            self.migrate_brands()
            self.migrate_products()
            self.migrate_inventory()
            self.migrate_sales()

            print("\n" + "=" * 60)
            print("✅ Migration completed successfully!")

            return True

        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            return False
        finally:
            if self.connection:
                self.connection.close()

if __name__ == "__main__":
    excel_file = "/Users/makaminski1337/Developer/LV/data/inputs/LaceLuxx Inventory May 26 2025 (2).xlsx"

    migrator = ExcelDataMigrator(excel_file)
    migrator.run_migration() 