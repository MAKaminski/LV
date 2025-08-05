#!/usr/bin/env python3
"""
LV Project Backend API
Feature 2: Input Screen Replacement
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI(
    title="LV Project API",
    description="Inventory Management System API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://makaminski1337@localhost/lv_project")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic models for API
class ProductBase(BaseModel):
    item_inventory_number: str
    name: str
    description: Optional[str] = None
    brand_id: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    product_id: str
    quantity: int = 0
    purchase_price: Optional[float] = None
    goal_earnings: Optional[float] = None
    floor_earnings: Optional[float] = None
    need_to_make: Optional[float] = None
    list_price: Optional[float] = None
    is_listed: bool = False
    notes: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: str
    quantity_sold: int = 1
    sell_price: float
    gross_amount_earned: Optional[float] = None
    net_profit_loss: Optional[float] = None
    percent_profit: Optional[float] = None
    date_sold: Optional[datetime] = None
    days_held: Optional[int] = None
    comps: Optional[str] = None
    notes: Optional[str] = None

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Routes

@app.get("/")
def read_root():
    return {"message": "LV Project API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Products API
@app.get("/api/products", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products with pagination"""
    # This would query the actual database
    # For now, return mock data
    return [
        {
            "id": str(uuid.uuid4()),
            "item_inventory_number": "LV001",
            "name": "Sample Product",
            "description": "A sample product",
            "brand_id": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]

@app.post("/api/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # This would insert into the actual database
    return {
        "id": str(uuid.uuid4()),
        **product.dict(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    # This would query the actual database
    return {
        "id": product_id,
        "item_inventory_number": "LV001",
        "name": "Sample Product",
        "description": "A sample product",
        "brand_id": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

# Inventory API
@app.get("/api/inventory", response_model=List[Inventory])
def get_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all inventory items"""
    return [
        {
            "id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4()),
            "quantity": 10,
            "purchase_price": 25.00,
            "goal_earnings": 50.00,
            "floor_earnings": 30.00,
            "need_to_make": 35.00,
            "list_price": 45.00,
            "is_listed": True,
            "notes": "Sample inventory item",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]

@app.post("/api/inventory", response_model=Inventory)
def create_inventory_item(inventory: InventoryCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    return {
        "id": str(uuid.uuid4()),
        **inventory.dict(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

# Sales API
@app.get("/api/sales", response_model=List[Sale])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sales"""
    return [
        {
            "id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4()),
            "quantity_sold": 1,
            "sell_price": 45.00,
            "gross_amount_earned": 45.00,
            "net_profit_loss": 20.00,
            "percent_profit": 80.0,
            "date_sold": datetime.now(),
            "days_held": 5,
            "comps": "Similar items sold for $40-50",
            "notes": "Sample sale",
            "created_at": datetime.now()
        }
    ]

@app.post("/api/sales", response_model=Sale)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """Create a new sale"""
    return {
        "id": str(uuid.uuid4()),
        **sale.dict(),
        "created_at": datetime.now()
    }

# Analytics API
@app.get("/api/analytics/top-products")
def get_top_products(db: Session = Depends(get_db)):
    """Get top selling products by revenue"""
    try:
        # Query top products by revenue from sales
        query = text("""
        SELECT 
            p.name as product_name,
            COALESCE(SUM(s.sell_price * s.quantity_sold), 0) as revenue,
            COALESCE(SUM(s.quantity_sold), 0) as units_sold
        FROM products p
        LEFT JOIN sales s ON p.id = s.product_id
        GROUP BY p.id, p.name
        ORDER BY revenue DESC
        LIMIT 10
        """)
        
        result = db.execute(query)
        top_by_revenue = [
            {
                "product_name": row.product_name,
                "revenue": float(row.revenue),
                "units_sold": int(row.units_sold)
            }
            for row in result
        ]
        
        return {"top_by_revenue": top_by_revenue}
    except Exception as e:
        print(f"Error in get_top_products: {e}")
        return {"top_by_revenue": []}

@app.get("/api/analytics/profit-analysis")
def get_profit_analysis(db: Session = Depends(get_db)):
    """Get profit analysis by brand (categories removed from schema)"""
    try:
        # Query profit by brand
        brand_query = text("""
        SELECT 
            b.name as brand,
            COALESCE(SUM(s.net_profit_loss), 0) as total_profit,
            COALESCE(AVG(s.percent_profit), 0) as avg_margin,
            COUNT(s.id) as total_sales
        FROM brands b
        LEFT JOIN products p ON b.id = p.brand_id
        LEFT JOIN sales s ON p.id = s.product_id
        GROUP BY b.id, b.name
        ORDER BY total_profit DESC
        """)
        
        brand_result = db.execute(brand_query)
        by_brand = [
            {
                "brand": row.brand,
                "total_profit": float(row.total_profit),
                "avg_margin": float(row.avg_margin),
                "total_sales": int(row.total_sales)
            }
            for row in brand_result
        ]
        
        # Since categories table was removed, we'll provide a summary instead
        summary_query = text("""
        SELECT 
            COUNT(DISTINCT p.id) as total_products,
            COUNT(s.id) as total_sales,
            COALESCE(SUM(s.net_profit_loss), 0) as total_profit,
            COALESCE(AVG(s.percent_profit), 0) as avg_margin
        FROM products p
        LEFT JOIN sales s ON p.id = s.product_id
        """)
        
        summary_result = db.execute(summary_query).fetchone()
        summary = {
            "total_products": int(summary_result.total_products) if summary_result else 0,
            "total_sales": int(summary_result.total_sales) if summary_result else 0,
            "total_profit": float(summary_result.total_profit) if summary_result else 0,
            "avg_margin": float(summary_result.avg_margin) if summary_result else 0
        }
        
        return {
            "by_brand": by_brand,
            "summary": summary
        }
    except Exception as e:
        print(f"Error in get_profit_analysis: {e}")
        return {
            "by_brand": [],
            "summary": {
                "total_products": 0,
                "total_sales": 0,
                "total_profit": 0,
                "avg_margin": 0
            }
        }

@app.get("/api/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get summary statistics"""
    try:
        # Total revenue
        revenue_query = text("""
        SELECT COALESCE(SUM(s.sell_price * s.quantity_sold), 0) as total_revenue
        FROM sales s
        """)
        revenue_result = db.execute(revenue_query).fetchone()
        total_revenue = float(revenue_result.total_revenue) if revenue_result else 0
        
        # Total profit
        profit_query = text("""
        SELECT COALESCE(SUM(s.net_profit_loss), 0) as total_profit
        FROM sales s
        """)
        profit_result = db.execute(profit_query).fetchone()
        total_profit = float(profit_result.total_profit) if profit_result else 0
        
        # Total products
        products_query = text("""
        SELECT COUNT(*) as total_products
        FROM products
        """)
        products_result = db.execute(products_query).fetchone()
        total_products = int(products_result.total_products) if products_result else 0
        
        # Total sales
        sales_query = text("""
        SELECT COUNT(*) as total_sales
        FROM sales
        """)
        sales_result = db.execute(sales_query).fetchone()
        total_sales = int(sales_result.total_sales) if sales_result else 0
        
        return {
            "totalRevenue": total_revenue,
            "totalProfit": total_profit,
            "totalProducts": total_products,
            "totalSales": total_sales
        }
    except Exception as e:
        print(f"Error in get_analytics_summary: {e}")
        return {
            "totalRevenue": 0,
            "totalProfit": 0,
            "totalProducts": 0,
            "totalSales": 0
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 