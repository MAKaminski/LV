# Updated ERD for Platform Luxx Base Data

## Overview
This document outlines the updated Entity Relationship Diagram (ERD) based on the new CSV data structure from "Platform Luxx Base Data.csv".

## Data Source Analysis

### CSV Structure
- **File**: `Platform Luxx Base Data.csv`
- **Records**: 774 items (775 total including header)
- **Format**: Single table with all inventory and sales data

### Key Fields
1. **Item Inventory #** - Unique identifier for each item
2. **Purchase_Date** - When item was purchased
3. **seller** - Who sold the item (seller information)
4. **Brand + Product Name** - Combined product information
5. **Brand** - Brand field (empty in CSV)
6. **Product_Name** - Product name field (empty in CSV)
7. **product description** - Detailed product description
8. **Quality** - Condition rating
9. **Purchase Price** - Cost to acquire item
10. **List Price** - Original listing price
11. **Sell price** - Final sale price
12. **Gross Amount Earned** - Revenue from sale
13. **Net Profit/Loss** - Profit or loss on sale
14. **Percent Profit** - Profit percentage
15. **Date Sold** - When item was sold
16. **Days Held** - How long item was held

## Updated Database Schema

### Core Entities

#### 1. Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    user_type VARCHAR(20) CHECK (user_type IN ('buyer', 'seller', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
- **Purpose**: Store seller and buyer information
- **Source**: `seller` field from CSV
- **Current Data**: 29 unique sellers identified

#### 2. Brands Table
```sql
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
- **Purpose**: Store brand information
- **Source**: Extracted from `Brand + Product Name` field
- **Current Data**: 89 unique brands identified

#### 3. Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_inventory_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    brand_id UUID REFERENCES brands(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
- **Purpose**: Store product information
- **Source**: `Brand + Product Name` and `product description` fields
- **Current Data**: 60 products migrated

### Inventory Management

#### 4. Inventory Table
```sql
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 0,
    purchase_price DECIMAL(10,2),
    list_price DECIMAL(10,2),
    is_listed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
- **Purpose**: Track current inventory levels
- **Source**: `Purchase Price` and `List Price` fields
- **Current Data**: 60 inventory records

### Transactions

#### 5. Sales Table
```sql
CREATE TABLE sales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id),
    seller_id UUID REFERENCES users(id),
    quantity_sold INTEGER NOT NULL DEFAULT 1,
    sell_price DECIMAL(10,2) NOT NULL,
    gross_amount_earned DECIMAL(10,2),
    net_profit_loss DECIMAL(10,2),
    percent_profit DECIMAL(5,2),
    date_sold DATE,
    days_held INTEGER,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
- **Purpose**: Track completed sales transactions
- **Source**: `Sell price`, `Gross Amount Earned`, `Net Profit/Loss`, `Date Sold`, `Days Held` fields
- **Current Data**: 29 sales records

## Data Migration Results

### Migration Summary
- **Total CSV Records**: 774 items
- **Brands Extracted**: 89 unique brands
- **Products Migrated**: 60 products
- **Inventory Records**: 60 records
- **Sales Records**: 29 completed sales
- **Sellers Identified**: 29 unique sellers

### Key Insights
1. **Brand Extraction**: Successfully extracted 89 brands from product names using pattern matching
2. **Sales Analysis**: 29 items have been sold (3.7% sell-through rate)
3. **Inventory Status**: 60 items currently in inventory
4. **Data Quality**: Handled various data formats including parentheses for negative values

### Data Processing Features
- **Money Value Parsing**: Handles `$`, commas, parentheses (negative values), and dash values
- **Brand Extraction**: Uses pattern matching for luxury brand names
- **Error Handling**: Robust error handling for malformed data
- **Batch Processing**: Commits data in batches to avoid transaction timeouts

## Weekly Update Process

### Automated Scripts
1. **`scripts/simple_csv_migrate.py`** - Main migration script
2. **`scripts/extract_brands.py`** - Brand extraction and linking
3. **`scripts/weekly_update.py`** - Weekly update routine

### Update Workflow
1. Place new CSV file in `data/inputs/`
2. Run `python3 scripts/weekly_update.py`
3. Script automatically:
   - Analyzes new data
   - Creates database backup
   - Migrates new data
   - Updates existing records

## Database Connection

### Local PostgreSQL Setup
- **Host**: localhost
- **Port**: 5432
- **Database**: lv_project
- **User**: makaminski1337
- **Password**: (empty)

### Connection Tools
- **SQLTools Extension**: Configured for VS Code/Cursor
- **Database Client JDBC**: Alternative connection option
- **Command Line**: `psql -d lv_project`

## Next Steps

### Immediate Actions
1. ✅ **Data Migration**: Complete
2. ✅ **Brand Extraction**: Complete
3. ✅ **Database Schema**: Updated
4. 🔄 **Backend API**: Update to use new schema
5. 🔄 **Frontend Dashboard**: Update to display real data

### Future Enhancements
1. **Advanced Analytics**: Profit analysis by brand, seller performance
2. **Inventory Management**: Stock level tracking, reorder alerts
3. **Sales Forecasting**: Predictive analytics for inventory planning
4. **User Management**: Seller/buyer portal functionality

## Technical Notes

### Data Quality Issues Handled
- Empty brand fields in CSV
- Various money value formats
- Missing or malformed dates
- Inconsistent text formatting

### Performance Optimizations
- Batch processing for large datasets
- Indexed foreign key relationships
- Efficient brand extraction algorithms
- Transaction management for data integrity

### Security Considerations
- Database backups before updates
- Input validation and sanitization
- Error logging and monitoring
- User authentication (future enhancement) 