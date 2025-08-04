-- LV Project Database Schema
-- Feature 1: ERD + Schema Development
-- Based on analysis of LaceLuxx Inventory Excel file

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CORE ENTITIES
-- =====================================================

-- Products table (normalized from product information)
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_inventory_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id UUID REFERENCES categories(id),
    brand_id UUID REFERENCES brands(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Brands table
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users table (buyers and sellers)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    user_type VARCHAR(20) CHECK (user_type IN ('buyer', 'seller', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INVENTORY MANAGEMENT
-- =====================================================

-- Inventory table (current stock levels)
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 0,
    purchase_price DECIMAL(10,2),
    goal_earnings DECIMAL(10,2),
    floor_earnings DECIMAL(10,2),
    need_to_make DECIMAL(10,2),
    list_price DECIMAL(10,2),
    is_listed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TRANSACTIONS
-- =====================================================

-- Orders table (from Sheet2 and For Listing PM)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(100) UNIQUE,
    order_numeric_id INTEGER,
    buyer_id UUID REFERENCES users(id),
    seller_id UUID REFERENCES users(id),
    processed_date DATE,
    order_status VARCHAR(50),
    order_style VARCHAR(50),
    order_currency VARCHAR(10) DEFAULT 'USD',
    subtotal DECIMAL(10,2),
    shipping_price DECIMAL(10,2),
    taxes DECIMAL(10,2),
    taxes_currency VARCHAR(10) DEFAULT 'USD',
    credits_applied DECIMAL(10,2),
    total DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Order Items table (line items in orders)
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id),
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    sold_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sales table (completed sales with profit tracking)
CREATE TABLE sales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id),
    order_id UUID REFERENCES orders(id),
    quantity_sold INTEGER NOT NULL DEFAULT 1,
    sell_price DECIMAL(10,2) NOT NULL,
    gross_amount_earned DECIMAL(10,2),
    net_profit_loss DECIMAL(10,2),
    percent_profit DECIMAL(5,2),
    date_sold DATE,
    days_held INTEGER,
    comps TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- PLATFORM SPECIFIC DATA
-- =====================================================

-- Platform Goals table (Poshmark, Whatnot, etc.)
CREATE TABLE platform_goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id),
    platform_name VARCHAR(50) NOT NULL,
    goal_price DECIMAL(10,2),
    floor_price DECIMAL(10,2),
    platform_fee DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ADMINISTRATIVE DATA
-- =====================================================

-- Admin Costs table
CREATE TABLE admin_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),
    cost_type VARCHAR(100),
    amount DECIMAL(10,2),
    description TEXT,
    date_incurred DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Product indexes
CREATE INDEX idx_products_item_inventory_number ON products(item_inventory_number);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_brand_id ON products(brand_id);

-- Inventory indexes
CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_inventory_is_listed ON inventory(is_listed);

-- Order indexes
CREATE INDEX idx_orders_order_id ON orders(order_id);
CREATE INDEX idx_orders_buyer_id ON orders(buyer_id);
CREATE INDEX idx_orders_seller_id ON orders(seller_id);
CREATE INDEX idx_orders_processed_date ON orders(processed_date);

-- Sales indexes
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_date_sold ON sales(date_sold);
CREATE INDEX idx_sales_order_id ON sales(order_id);

-- Platform goals indexes
CREATE INDEX idx_platform_goals_product_id ON platform_goals(product_id);
CREATE INDEX idx_platform_goals_platform_name ON platform_goals(platform_name);

-- =====================================================
-- TRIGGERS FOR UPDATED_AT
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with updated_at
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_inventory_updated_at BEFORE UPDATE ON inventory FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_platform_goals_updated_at BEFORE UPDATE ON platform_goals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Clothing', 'Apparel and fashion items'),
('Accessories', 'Jewelry, bags, and accessories'),
('Home & Garden', 'Home decor and garden items'),
('Electronics', 'Electronic devices and gadgets'),
('Books & Media', 'Books, DVDs, and media');

-- Insert sample brands
INSERT INTO brands (name, description) VALUES
('LaceLuxx', 'Main brand for the business'),
('Generic', 'Generic or unbranded items'),
('Vintage', 'Vintage and retro items'),
('Designer', 'High-end designer items'); 