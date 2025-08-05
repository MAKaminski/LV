# Database Schema Documentation

## Current Database Schema (CSV-Optimized)

The LV Project database has been optimized for the Platform Luxx Base Data.csv file, with 5 essential tables that perfectly match the CSV data structure.

## Core Tables

### 1. Users Table
**Purpose**: Store seller and buyer information
**Records**: 126 users
**Source**: `seller` field from CSV

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

### 2. Brands Table
**Purpose**: Store brand information
**Records**: 89 luxury brands
**Source**: Extracted from "Brand + Product Name" field

```sql
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Products Table
**Purpose**: Store product information
**Records**: 60 products
**Source**: "Brand + Product Name" and "product description" fields

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

### 4. Inventory Table
**Purpose**: Track current inventory levels
**Records**: 60 records
**Source**: "Purchase Price" and "List Price" fields

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

### 5. Sales Table
**Purpose**: Track completed sales transactions
**Records**: 29 sales
**Source**: "Sell price", "Gross Amount Earned", "Net Profit/Loss" fields

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

## Removed Tables

The following tables were removed during database cleanup as they were not needed for the CSV data structure:

- **admin_costs**: Administrative costs tracking (not in CSV)
- **categories**: Product categories (not used, organized by brands)
- **order_items**: Order line items (CSV uses direct sales)
- **orders**: Order management (CSV tracks individual sales)
- **platform_goals**: Multi-platform selling goals (not in CSV)

## Data Relationships

```
users (126 records)
├── brands (89 records)
│   └── products (60 records)
│       ├── inventory (60 records)
│       └── sales (29 records)
```

## Key Indexes

```sql
-- Performance optimization indexes
CREATE INDEX idx_products_item_inventory_number ON products(item_inventory_number);
CREATE INDEX idx_products_brand_id ON products(brand_id);
CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_inventory_is_listed ON inventory(is_listed);
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_date_sold ON sales(date_sold);
CREATE INDEX idx_sales_seller_id ON sales(seller_id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_user_type ON users(user_type);
```

## Data Migration Results

### CSV Source Analysis
- **File**: Platform Luxx Base Data.csv
- **Total Records**: 774 items
- **Data Quality**: Handled various money formats and inconsistencies

### Migration Statistics
- **Brands Extracted**: 89 unique luxury brands
- **Products Migrated**: 60 products with complete information
- **Inventory Records**: 60 records with pricing
- **Sales Records**: 29 completed sales with profit analysis
- **Users Identified**: 126 unique sellers/buyers

### Data Processing Features
- **Money Value Parsing**: Handles $, commas, parentheses (negative values)
- **Brand Extraction**: Intelligent pattern matching for luxury brands
- **Error Handling**: Robust handling of malformed data
- **Batch Processing**: Efficient large dataset processing

## Analytics Queries

### Customer Analytics
```sql
-- Top customers by revenue
SELECT 
    u.id as customer_id,
    u.full_name as customer_name,
    COUNT(s.id) as total_orders,
    SUM(s.gross_amount_earned) as total_spend,
    SUM(s.quantity_sold) as total_units,
    AVG(s.gross_amount_earned) as avg_order_value
FROM users u
LEFT JOIN sales s ON u.id = s.seller_id
WHERE u.user_type = 'buyer'
GROUP BY u.id, u.full_name
ORDER BY total_spend DESC;
```

### Sales Timing Analytics
```sql
-- Daily sales analysis
SELECT 
    EXTRACT(DOW FROM s.date_sold) as day_of_week,
    COUNT(s.id) as units_sold,
    SUM(s.gross_amount_earned) as total_revenue,
    AVG(s.sell_price) as avg_price_per_unit
FROM sales s
WHERE s.date_sold IS NOT NULL
GROUP BY EXTRACT(DOW FROM s.date_sold)
ORDER BY total_revenue DESC;
```

### Product Analytics
```sql
-- Top selling products
SELECT 
    p.name as product_name,
    b.name as brand_name,
    COUNT(s.id) as units_sold,
    SUM(s.gross_amount_earned) as total_revenue,
    AVG(s.sell_price) as avg_sell_price,
    AVG(s.net_profit_loss) as avg_profit
FROM products p
LEFT JOIN brands b ON p.brand_id = b.id
LEFT JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name, b.name
ORDER BY total_revenue DESC;
```

### Brand Analytics
```sql
-- Brand performance analysis
SELECT 
    b.name as brand_name,
    COUNT(DISTINCT p.id) as total_products,
    COUNT(s.id) as total_sales,
    SUM(s.gross_amount_earned) as total_revenue,
    SUM(s.net_profit_loss) as total_profit,
    AVG(s.percent_profit) as avg_profit_percentage,
    AVG(s.days_held) as avg_days_to_sell
FROM brands b
LEFT JOIN products p ON b.id = p.brand_id
LEFT JOIN sales s ON p.id = s.product_id
GROUP BY b.id, b.name
ORDER BY total_profit DESC;
```

## Maintenance

### Weekly Updates
The system includes automated weekly update scripts:
- **`scripts/weekly_update.py`**: Automated CSV processing
- **`scripts/simple_csv_migrate.py`**: Main migration script
- **`scripts/extract_brands.py`**: Brand extraction and linking

### Database Cleanup
- **`scripts/cleanup_database.py`**: Removed unnecessary tables
- **Documentation**: Complete cleanup summary available

## Connection Information

### Local PostgreSQL Setup
- **Host**: localhost
- **Port**: 5432
- **Database**: lv_project
- **User**: makaminski1337
- **Password**: (empty)

### Connection Tools
- **Database Client JDBC**: Configured for VS Code/Cursor
- **Command Line**: `psql -d lv_project`
- **Python**: `psycopg2` with connection parameters

---

**This schema is optimized for CSV-based inventory management with comprehensive analytics capabilities.** 