#!/usr/bin/env python3
"""
Weekly Data Update Script for LV Project
Routine script to update database with new CSV data
"""

import os
import sys
import pandas as pd
from datetime import datetime
from csv_migrator import CSVDataMigrator

def get_latest_csv_file():
    """Get the most recent CSV file from the inputs directory"""
    inputs_dir = "data/inputs"
    
    if not os.path.exists(inputs_dir):
        print(f"❌ Inputs directory not found: {inputs_dir}")
        return None
    
    csv_files = [f for f in os.listdir(inputs_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"❌ No CSV files found in {inputs_dir}")
        return None
    
    # Get the most recent file by modification time
    latest_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(inputs_dir, f)))
    latest_path = os.path.join(inputs_dir, latest_file)
    
    print(f"📁 Found latest CSV file: {latest_file}")
    return latest_path

def backup_database():
    """Create a backup of the current database"""
    backup_dir = "data/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/lv_project_backup_{timestamp}.sql"
    
    print(f"💾 Creating database backup: {backup_file}")
    
    try:
        os.system(f"pg_dump -d lv_project > {backup_file}")
        print("✅ Database backup created successfully")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def analyze_csv_data(csv_file):
    """Analyze the CSV data before migration"""
    print(f"\n📊 Analyzing CSV data: {csv_file}")
    
    try:
        df = pd.read_csv(csv_file)
        
        print(f"  📈 Total records: {len(df)}")
        print(f"  🏷️  Unique brands: {df['Brand'].nunique()}")
        print(f"  👥 Unique sellers: {df['seller'].nunique()}")
        
        # Count sold items
        sold_items = df[df[' Sell price '].notna() & (df[' Sell price '] != '')]
        print(f"  💰 Sold items: {len(sold_items)}")
        
        # Count unsold items
        unsold_items = df[df[' Sell price '].isna() | (df[' Sell price '] == '')]
        print(f"  📦 Unsold items: {len(unsold_items)}")
        
        # Calculate total revenue and profit
        if len(sold_items) > 0:
            total_revenue = sold_items[' Gross Amount Earned '].apply(
                lambda x: float(str(x).replace('$', '').replace(',', '')) if pd.notna(x) and str(x).strip() else 0
            ).sum()
            
            total_profit = sold_items[' Net Profit/Loss '].apply(
                lambda x: float(str(x).replace('$', '').replace(',', '')) if pd.notna(x) and str(x).strip() else 0
            ).sum()
            
            print(f"  💵 Total revenue: ${total_revenue:,.2f}")
            print(f"  💸 Total profit: ${total_profit:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing CSV: {e}")
        return False

def main():
    """Main weekly update process"""
    print("🔄 LV Project Weekly Data Update")
    print("=" * 50)
    
    # Step 1: Get latest CSV file
    csv_file = get_latest_csv_file()
    if not csv_file:
        print("❌ No CSV file found. Please place your latest data file in data/inputs/")
        return False
    
    # Step 2: Analyze the data
    if not analyze_csv_data(csv_file):
        return False
    
    # Step 3: Create backup
    if not backup_database():
        print("⚠️  Continuing without backup...")
    
    # Step 4: Run migration
    print(f"\n🚀 Starting migration with: {csv_file}")
    
    migrator = CSVDataMigrator(csv_file)
    success = migrator.run_migration()
    
    if success:
        print("\n✅ Weekly update completed successfully!")
        print("📊 Your database has been updated with the latest data.")
        print("🌐 Check your dashboard at http://localhost:3000")
    else:
        print("\n❌ Weekly update failed!")
        print("🔧 Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 