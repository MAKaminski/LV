# Feature 1: ERD + Schema Development

## Objective
Convert Excel-based inventory management to a normalized PostgreSQL database system.

## Core Entities Identified
Based on typical inventory management requirements:

### Primary Entities
1. **Products** - Core product information
2. **Brands** - Product brands/manufacturers
3. **Categories** - Product categories
4. **Inventory** - Current stock levels
5. **Purchases** - Purchase transactions
6. **Sales** - Sales transactions
7. **Suppliers** - Product suppliers
8. **Quality Levels** - Product quality grades

### Supporting Entities
1. **Users** - System users
2. **Locations** - Storage locations
3. **Transactions** - Audit trail

## ERD Design Principles
- **Normalization**: 3NF to minimize redundancy
- **Referential Integrity**: Proper foreign key relationships
- **Audit Trail**: Track all changes with timestamps
- **Scalability**: Design for future growth

## Database Schema Overview

### Core Tables
```sql
-- Products table
products (
  id, name, sku, description, 
  brand_id, category_id, 
  created_at, updated_at
)

-- Inventory table
inventory (
  id, product_id, quantity, 
  location_id, quality_level_id,
  min_stock_level, max_stock_level,
  created_at, updated_at
)

-- Purchases table
purchases (
  id, product_id, supplier_id,
  quantity, unit_cost, total_cost,
  purchase_date, received_date,
  created_at, updated_at
)

-- Sales table
sales (
  id, product_id, quantity,
  unit_price, total_price,
  sale_date, created_at, updated_at
)
```

## Implementation Steps
1. **Schema Design**: Create normalized table structures
2. **Migration Scripts**: Convert Excel data to database
3. **Data Validation**: Ensure data integrity
4. **Indexing**: Optimize query performance
5. **Testing**: Validate schema with sample data

## Success Criteria
- ✅ All Excel data successfully migrated
- ✅ Normalized schema eliminates redundancy
- ✅ Proper foreign key relationships established
- ✅ Audit trail for all transactions
- ✅ Performance optimized with proper indexing 