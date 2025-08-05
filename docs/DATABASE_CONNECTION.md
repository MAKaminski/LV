# Database Connection Guide

## 🔗 LV Project Database Connection Details

### **Connection Information:**
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `lv_project`
- **Username**: `makaminski1337`
- **Password**: (none - using local authentication)
- **Connection String**: `postgresql://makaminski1337@localhost:5432/lv_project`

---

## 📊 SQL Tools Setup

### **1. VS Code SQLTools Extension**

1. Install the **SQLTools** extension in VS Code
2. Open Command Palette (`Cmd+Shift+P`)
3. Run: `SQLTools: Add Connection`
4. Select **PostgreSQL**
5. Fill in the details:
   - **Name**: `LV Project Database`
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `lv_project`
   - **Username**: `makaminski1337`
   - **Password**: (leave empty)

### **2. DBeaver (Universal Database Tool)**

1. Download and install DBeaver
2. Click **New Database Connection**
3. Select **PostgreSQL**
4. Fill in connection details:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `lv_project`
   - **Username**: `makaminski1337`
   - **Password**: (leave empty)

### **3. TablePlus (Mac Native)**

1. Download and install TablePlus
2. Click **Create a new connection**
3. Select **PostgreSQL**
4. Fill in:
   - **Name**: `LV Project`
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `lv_project`
   - **User**: `makaminski1337`
   - **Password**: (leave empty)

### **4. pgAdmin (PostgreSQL Admin)**

1. Download and install pgAdmin
2. Right-click **Servers** → **Create** → **Server**
3. General tab:
   - **Name**: `LV Project`
4. Connection tab:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `lv_project`
   - **Username**: `makaminski1337`
   - **Password**: (leave empty)

---

## 🐍 Python Database Explorer

We've created a Python script to explore the database:

```bash
# Run the database explorer
python3 scripts/db_connect.py
```

This script will show you:
- Database table information
- Data summaries
- Sample data from each table
- Example queries

---

## 📈 Quick Database Queries

### **View All Products:**
```sql
SELECT name, item_inventory_number, description 
FROM products 
LIMIT 10;
```

### **View Sales:**
```sql
SELECT p.name, s.sell_price, s.net_profit_loss, s.date_sold
FROM sales s
JOIN products p ON s.product_id = p.id;
```

### **View Inventory:**
```sql
SELECT p.name, i.quantity, i.purchase_price, i.list_price
FROM inventory i
JOIN products p ON i.product_id = p.id
WHERE i.quantity > 0
LIMIT 10;
```

### **Top Products by Value:**
```sql
SELECT 
    p.name,
    i.quantity,
    i.purchase_price,
    (i.quantity * i.purchase_price) as total_value
FROM products p
JOIN inventory i ON p.id = i.product_id
WHERE i.quantity > 0
ORDER BY total_value DESC
LIMIT 10;
```

---

## 🔧 Troubleshooting

### **Connection Issues:**

1. **Make sure PostgreSQL is running:**
   ```bash
   brew services list | grep postgresql
   ```

2. **Start PostgreSQL if needed:**
   ```bash
   brew services start postgresql@15
   ```

3. **Test connection:**
   ```bash
   psql -d lv_project -c "SELECT current_database();"
   ```

### **Permission Issues:**

If you get permission errors, make sure you're using the correct user:
```bash
# Check current user
whoami

# Connect as the correct user
psql -U makaminski1337 -d lv_project
```

---

## 📊 Database Schema Overview

### **Main Tables:**
- **products**: 766 items (your inventory)
- **inventory**: 766 records (stock levels)
- **sales**: 1 record (completed sales)
- **categories**: 11 categories
- **brands**: 4 brands

### **Key Relationships:**
- `products` → `categories` (via category_id)
- `products` → `brands` (via brand_id)
- `inventory` → `products` (via product_id)
- `sales` → `products` (via product_id)

---

## 🚀 Quick Start Commands

```bash
# Connect to database
psql -d lv_project

# View all tables
\dt

# View table structure
\d products

# Run a query
SELECT COUNT(*) FROM products;

# Exit
\q
```

Your database is ready to use with any SQL tool! 🎉 