#!/usr/bin/env python3
"""
Simple CSV Migration Script
Handles errors better and processes data in smaller batches
"""

import pandas as pd
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

def parse_money_value(value_str):
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

def main():
    """Main migration function"""
    print("🚀 Starting Simple CSV Migration")
    print("=" * 50)
    
    # Connect to database
    try:
        conn = psycopg2.connect(**get_db_config())
        print("✅ Connected to database")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    cursor = conn.cursor()
    
    # Read CSV file
    csv_file = "/Users/makaminski1337/Developer/LV/data/inputs/Platform Luxx Base Data.csv"
    try:
        df = pd.read_csv(csv_file)
        print(f"📊 Loaded {len(df)} records from CSV")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Clear existing data
    print("\n🧹 Clearing existing data...")
    try:
        cursor.execute("DELETE FROM sales")
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM brands")
        conn.commit()
        print("✅ Cleared existing data")
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        return
    
    # Migrate brands first
    print("\n🏷️  Migrating brands...")
    brands_migrated = 0
    unique_brands = df['Brand'].dropna().unique()
    
    for brand in unique_brands:
        if brand and str(brand).strip():
            try:
                cursor.execute("INSERT INTO brands (name, description) VALUES (%s, %s)", 
                             (brand, f"Brand: {brand}"))
                brands_migrated += 1
            except Exception as e:
                print(f"  ⚠️  Error adding brand {brand}: {e}")
                continue
    
    conn.commit()
    print(f"✅ Migrated {brands_migrated} brands")
    
    # Migrate products
    print("\n📦 Migrating products...")
    products_migrated = 0
    
    for _, row in df.iterrows():
        try:
            item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
            brand_product_name = str(row['Brand + Product Name']) if pd.notna(row['Brand + Product Name']) else ''
            brand = str(row['Brand']) if pd.notna(row['Brand']) else ''
            
            if item_number and brand_product_name:
                # Get brand ID
                brand_id = None
                if brand:
                    cursor.execute("SELECT id FROM brands WHERE name = %s", (brand,))
                    brand_result = cursor.fetchone()
                    if brand_result:
                        brand_id = brand_result[0]
                
                # Create product name
                name = brand_product_name if brand_product_name else ''
                
                cursor.execute(
                    "INSERT INTO products (item_inventory_number, name, description, brand_id) VALUES (%s, %s, %s, %s)",
                    (item_number, name, f"Product: {name}", brand_id)
                )
                products_migrated += 1
                
                # Commit every 10 products to avoid long transactions
                if products_migrated % 10 == 0:
                    conn.commit()
                    print(f"  ✅ Migrated {products_migrated} products so far...")
                
        except Exception as e:
            print(f"  ⚠️  Error processing product {row.get('Item Inventory #', 'Unknown')}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Migrated {products_migrated} products")
    
    # Migrate inventory
    print("\n📊 Migrating inventory...")
    inventory_migrated = 0
    
    for _, row in df.iterrows():
        try:
            item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
            
            if item_number:
                # Get product ID
                cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                product_result = cursor.fetchone()
                
                if product_result:
                    product_id = product_result[0]
                    
                    # Parse prices
                    purchase_price = parse_money_value(row[' Purchase Price '])
                    list_price = parse_money_value(row[' List Price '])
                    
                    cursor.execute(
                        "INSERT INTO inventory (product_id, quantity, purchase_price, list_price, is_listed) VALUES (%s, %s, %s, %s, %s)",
                        (product_id, 1, purchase_price, list_price, True)
                    )
                    inventory_migrated += 1
                    
                    # Commit every 10 records
                    if inventory_migrated % 10 == 0:
                        conn.commit()
                        print(f"  ✅ Migrated {inventory_migrated} inventory records so far...")
                
        except Exception as e:
            print(f"  ⚠️  Error processing inventory for {row.get('Item Inventory #', 'Unknown')}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Migrated {inventory_migrated} inventory records")
    
    # Migrate sales
    print("\n💰 Migrating sales...")
    sales_migrated = 0
    
    for _, row in df.iterrows():
        try:
            item_number = str(row['Item Inventory #']) if pd.notna(row['Item Inventory #']) else None
            
            if item_number:
                # Get product ID
                cursor.execute("SELECT id FROM products WHERE item_inventory_number = %s", (item_number,))
                product_result = cursor.fetchone()
                
                if product_result:
                    product_id = product_result[0]
                    
                    # Parse sales data
                    sell_price = parse_money_value(row[' Sell price '])
                    gross_amount = parse_money_value(row[' Gross Amount Earned '])
                    net_profit = parse_money_value(row[' Net Profit/Loss '])
                    
                    # Only create sales records if there's a sell price
                    if sell_price and sell_price > 0:
                        cursor.execute(
                            "INSERT INTO sales (product_id, quantity_sold, sell_price, gross_amount_earned, net_profit_loss) VALUES (%s, %s, %s, %s, %s)",
                            (product_id, 1, sell_price, gross_amount, net_profit)
                        )
                        sales_migrated += 1
                        
                        # Commit every 10 records
                        if sales_migrated % 10 == 0:
                            conn.commit()
                            print(f"  ✅ Migrated {sales_migrated} sales records so far...")
                
        except Exception as e:
            print(f"  ⚠️  Error processing sale for {row.get('Item Inventory #', 'Unknown')}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Migrated {sales_migrated} sales records")
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 Migration Summary:")
    print(f"  🏷️  Brands: {brands_migrated}")
    print(f"  📦 Products: {products_migrated}")
    print(f"  📊 Inventory: {inventory_migrated}")
    print(f"  💰 Sales: {sales_migrated}")
    print("✅ Migration completed successfully!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main() 