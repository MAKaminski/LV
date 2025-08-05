#!/usr/bin/env python3
"""
Script to migrate CSV data to PostgreSQL database
Updated for Platform Luxx Base Data.csv format
"""

import pandas as pd
import psycopg2
import os
import json
from datetime import datetime
import uuid
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class CSVDataMigrator:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
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
            'user': os.getenv('POSTGRES_USER', 'makaminski1337'),
            'password': os.getenv('POSTGRES_PASSWORD', ''),
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

    def clear_existing_data(self):
        """Clear existing data to start fresh"""
        print("\n🧹 Clearing existing data...")
        try:
            cursor = self.connection.cursor()
            
            # Clear in reverse order of dependencies
            cursor.execute("DELETE FROM sales")
            cursor.execute("DELETE FROM inventory")
            cursor.execute("DELETE FROM products")
            cursor.execute("DELETE FROM categories")
            cursor.execute("DELETE FROM brands")
            
            self.connection.commit()
            cursor.close()
            print("✅ Cleared existing data")
        except Exception as e:
            print(f"❌ Error clearing data: {str(e)}")

    def parse_money_value(self, value_str):
        """Parse money values from CSV, handling various formats"""
        if pd.isna(value_str) or value_str == '' or str(value_str).strip() == '':
            return None
        
        value_str = str(value_str).strip()
        
        # Handle empty or dash values
        if value_str == '-' or value_str == '':
            return None
        
        # Handle parentheses (negative values)
        if value_str.startswith('(') and value_str.endswith(')'):
            # Extract the number and make it negative
            number_str = value_str[1:-1].replace('$', '').replace(',', '').strip()
            try:
                return -float(number_str)
            except:
                return None
        
        # Handle regular positive values
        try:
            # Remove $ and commas
            clean_value = value_str.replace('$', '').replace(',', '').strip()
            return float(clean_value) if clean_value else None
        except:
            return None

    def migrate_sellers(self):
        """Migrate unique sellers from CSV"""
        print("\n👥 Migrating sellers...")
        
        try:
            df = pd.read_csv(self.csv_file_path)
            
            # Extract unique sellers
            sellers = df['seller'].dropna().unique()
            
            cursor = self.connection.cursor()
            
            for seller in sellers:
                if seller and str(seller).strip() and str(seller).lower() != 'na':
                    # Check if seller already exists
                    cursor.execute("SELECT id FROM users WHERE username = %s", (str(seller),))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO users (username, user_type, full_name) VALUES (%s, %s, %s)",
                            (str(seller), 'seller', f"Seller: {str(seller)}")
                        )
                        print(f"  ✅ Added seller: {seller}")

            self.connection.commit()
            cursor.close()
            print(f"✅ Migrated {len(sellers)} sellers")

        except Exception as e:
            print(f"❌ Error migrating sellers: {str(e)}")

    def migrate_brands(self):
        """Migrate brands from CSV data"""
        print("\n🏷️  Migrating brands...")

        try:
            df = pd.read_csv(self.csv_file_path)
            
            # Extract unique brands
            brands = df['Brand'].dropna().unique()

            cursor = self.connection.cursor()

            for brand in brands:
                if brand and str(brand).strip():
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
        """Migrate products from CSV"""
        print("\n📦 Migrating products...")

        try:
            df = pd.read_csv(self.csv_file_path)
            cursor = self.connection.cursor()

            products_migrated = 0

            for _, row in df.iterrows():
                try:
                    item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
                    brand_product_name = str(row['Brand + Product Name']) if pd.notna(row['Brand + Product Name']) else ''
                    brand = str(row['Brand']) if pd.notna(row['Brand']) else ''
                    product_name = str(row['Product_Name']) if pd.notna(row['Product_Name']) else ''
                    description = str(row['product description']) if pd.notna(row['product description']) else ''
                    quality = str(row[' Quality ']) if pd.notna(row[' Quality ']) else ''

                    if item_number and brand_product_name:
                        # Get brand ID
                        brand_id = None
                        if brand:
                            cursor.execute("SELECT id FROM brands WHERE name = %s", (brand,))
                            brand_result = cursor.fetchone()
                            if brand_result:
                                brand_id = brand_result[0]

                        # Create product name (use Brand + Product Name if available, otherwise Product_Name)
                        name = brand_product_name if brand_product_name else product_name
                        
                        # Combine description with quality
                        full_description = description
                        if quality:
                            full_description = f"{description} Quality: {quality}".strip()

                        cursor.execute(
                            """INSERT INTO products 
                               (item_inventory_number, name, description, brand_id)
                               VALUES (%s, %s, %s, %s)""",
                            (item_number, name, full_description, brand_id)
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
        """Migrate inventory data from CSV"""
        print("\n📊 Migrating inventory...")

        try:
            df = pd.read_csv(self.csv_file_path)
            cursor = self.connection.cursor()

            inventory_migrated = 0

            for _, row in df.iterrows():
                try:
                    item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
                    
                    # Parse purchase price
                    purchase_price = self.parse_money_value(row[' Purchase Price '])
                    
                    # Parse list price
                    list_price = self.parse_money_value(row[' List Price '])

                    if item_number:
                        # Get product ID
                        cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                        product_result = cursor.fetchone()

                        if product_result:
                            product_id = product_result[0]

                            cursor.execute(
                                """INSERT INTO inventory 
                                   (product_id, quantity, purchase_price, list_price, is_listed)
                                   VALUES (%s, %s, %s, %s, %s)""",
                                (product_id, 1, purchase_price, list_price, True)
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
        """Migrate sales data from CSV"""
        print("\n💰 Migrating sales...")

        try:
            df = pd.read_csv(self.csv_file_path)
            cursor = self.connection.cursor()

            sales_migrated = 0

            for _, row in df.iterrows():
                try:
                    item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
                    
                    # Parse sell price
                    sell_price = self.parse_money_value(row[' Sell price '])
                    
                    # Parse gross amount
                    gross_amount = self.parse_money_value(row[' Gross Amount Earned '])
                    
                    # Parse net profit
                    net_profit = self.parse_money_value(row[' Net Profit/Loss '])
                    
                    # Parse percent profit
                    percent_profit_str = str(row['Percent Profit']) if pd.notna(row['Percent Profit']) else '0%'
                    percent_profit = 0
                    if percent_profit_str and percent_profit_str != '0%':
                        try:
                            percent_profit = float(percent_profit_str.replace('%', '').strip())
                        except:
                            percent_profit = 0
                    
                    # Parse date sold
                    date_sold_str = str(row['Date Sold']) if pd.notna(row['Date Sold']) else None
                    date_sold = None
                    if date_sold_str and date_sold_str.strip():
                        try:
                            date_sold = pd.to_datetime(date_sold_str).date()
                        except:
                            pass
                    
                    # Parse days held
                    days_held_str = str(row['Days Held']) if pd.notna(row['Days Held']) else '0'
                    days_held = None
                    if days_held_str and days_held_str.strip() != '0':
                        try:
                            days_held = int(float(days_held_str.strip()))
                        except:
                            days_held = None

                    if item_number and sell_price and sell_price > 0:
                        # Get product ID
                        cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                        product_result = cursor.fetchone()

                        if product_result:
                            product_id = product_result[0]

                            cursor.execute(
                                """INSERT INTO sales
                                   (product_id, quantity_sold, sell_price, gross_amount_earned,
                                    net_profit_loss, percent_profit, date_sold, days_held)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (product_id, 1, sell_price, gross_amount, net_profit,
                                 percent_profit, date_sold, days_held)
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
        print("🚀 Starting CSV to Database Migration")
        print("=" * 60)

        if not self.connect_db():
            return False

        try:
            # Clear existing data
            self.clear_existing_data()
            
            # Run migrations in order
            self.migrate_sellers()
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
    csv_file = "/Users/makaminski1337/Developer/LV/data/inputs/Platform Luxx Base Data.csv"

    migrator = CSVDataMigrator(csv_file)
    migrator.run_migration() 