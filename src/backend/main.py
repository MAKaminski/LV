#!/usr/bin/env python3
"""
LV Project Backend API
Feature 2: Input Screen Replacement
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:your_secure_password@localhost/lv_project")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic models for API
class ProductBase(BaseModel):
    item_inventory_number: str
    name: str
    description: Optional[str] = None
    category_id: Optional[str] = None
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
            "category_id": None,
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
        "category_id": None,
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
    return {
        "top_by_revenue": [
            {"product_name": "Product A", "revenue": 1500.00, "units_sold": 30},
            {"product_name": "Product B", "revenue": 1200.00, "units_sold": 24},
            {"product_name": "Product C", "revenue": 900.00, "units_sold": 18}
        ],
        "top_by_margin": [
            {"product_name": "Product A", "margin": 80.5, "profit": 1200.00},
            {"product_name": "Product B", "margin": 75.2, "profit": 900.00},
            {"product_name": "Product C", "margin": 70.1, "profit": 630.00}
        ]
    }

@app.get("/api/analytics/profit-analysis")
def get_profit_analysis(db: Session = Depends(get_db)):
    """Get profit analysis by brand and category"""
    return {
        "by_brand": [
            {"brand": "LaceLuxx", "total_profit": 2500.00, "avg_margin": 75.5},
            {"brand": "Generic", "total_profit": 1800.00, "avg_margin": 65.2},
            {"brand": "Designer", "total_profit": 3200.00, "avg_margin": 85.1}
        ],
        "by_category": [
            {"category": "Clothing", "total_profit": 2000.00, "avg_margin": 70.5},
            {"category": "Accessories", "total_profit": 1500.00, "avg_margin": 80.2},
            {"category": "Home & Garden", "total_profit": 1000.00, "avg_margin": 65.8}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 