#!/usr/bin/env python3
"""
Extract brands from Brand + Product Name column and update database
"""

import pandas as pd
import psycopg2
import os
import re
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

def extract_brand_from_name(product_name):
    """Extract brand name from product name"""
    if pd.isna(product_name) or not product_name:
        return None
    
    # Common luxury brands to look for
    luxury_brands = [
        'Louis Vuitton', 'Chanel', 'Gucci', 'Prada', 'Hermès', 'Fendi', 'Bottega Veneta',
        'Saint Laurent', 'YSL', 'Balenciaga', 'Celine', 'Dior', 'Givenchy', 'Chloé',
        'Tory Burch', 'MCM', 'Furla', 'Badgley Mischka', 'DKNY', 'Valentino',
        'Bottega Veneta', 'Balenciaga', 'Celine', 'Dior', 'Givenchy', 'Chloé',
        'Morroccan Oil', 'Disney', 'Tiffany', 'Christian Dior', 'Ferragamo'
    ]
    
    product_name = str(product_name).strip()
    
    # Check for exact brand matches
    for brand in luxury_brands:
        if brand.lower() in product_name.lower():
            return brand
    
    # If no exact match, try to extract the first word as brand
    words = product_name.split()
    if words:
        # Common patterns for brand names
        potential_brand = words[0]
        if len(potential_brand) > 2 and potential_brand[0].isupper():
            return potential_brand
    
    return None

def main():
    """Main function to extract brands and update database"""
    print("🏷️  Extracting brands from product names...")
    
    # Read CSV
    csv_file = "/Users/makaminski1337/Developer/LV/data/inputs/Platform Luxx Base Data.csv"
    df = pd.read_csv(csv_file)
    
    # Extract brands from product names
    brands_found = set()
    brand_mapping = {}
    
    for _, row in df.iterrows():
        product_name = row['Brand + Product Name']
        brand = extract_brand_from_name(product_name)
        if brand:
            brands_found.add(brand)
            brand_mapping[row['Item Inventory #']] = brand
    
    print(f"📊 Found {len(brands_found)} unique brands:")
    for brand in sorted(brands_found):
        print(f"  - {brand}")
    
    # Connect to database
    conn = psycopg2.connect(**get_db_config())
    cursor = conn.cursor()
    
    # Insert brands
    print(f"\n💾 Inserting {len(brands_found)} brands into database...")
    brands_inserted = 0
    
    for brand in brands_found:
        try:
            cursor.execute("INSERT INTO brands (name, description) VALUES (%s, %s)", 
                         (brand, f"Brand: {brand}"))
            brands_inserted += 1
        except Exception as e:
            print(f"  ⚠️  Error inserting brand {brand}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Inserted {brands_inserted} brands")
    
    # Update products with brand_id
    print(f"\n🔗 Updating products with brand information...")
    products_updated = 0
    
    for item_number, brand in brand_mapping.items():
        try:
            # Get brand ID
            cursor.execute("SELECT id FROM brands WHERE name = %s", (brand,))
            brand_result = cursor.fetchone()
            
            if brand_result:
                brand_id = brand_result[0]
                
                # Update product
                cursor.execute("UPDATE products SET brand_id = %s WHERE item_inventory_number = %s", 
                             (brand_id, str(item_number)))
                products_updated += 1
                
        except Exception as e:
            print(f"  ⚠️  Error updating product {item_number}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Updated {products_updated} products with brand information")
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 Brand Extraction Summary:")
    print(f"  🏷️  Brands found: {len(brands_found)}")
    print(f"  🏷️  Brands inserted: {brands_inserted}")
    print(f"  📦 Products updated: {products_updated}")
    print("✅ Brand extraction completed!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main() 