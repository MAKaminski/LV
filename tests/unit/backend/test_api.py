#!/usr/bin/env python3
"""
Unit tests for FastAPI backend
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/backend'))

from main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Test health and basic endpoints"""
    
    def test_read_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "LV Project API", "version": "1.0.0"}
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"

class TestProductsAPI:
    """Test products API endpoints"""
    
    def test_get_products(self):
        """Test getting all products"""
        response = client.get("/api/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        if products:  # If there are products
            assert "id" in products[0]
            assert "item_inventory_number" in products[0]
            assert "name" in products[0]
    
    def test_create_product(self):
        """Test creating a new product"""
        product_data = {
            "item_inventory_number": "TEST001",
            "name": "Test Product",
            "description": "A test product"
        }
        response = client.post("/api/products", json=product_data)
        assert response.status_code == 200
        product = response.json()
        assert product["item_inventory_number"] == "TEST001"
        assert product["name"] == "Test Product"
        assert "id" in product
    
    def test_get_product_by_id(self):
        """Test getting a specific product"""
        # First create a product
        product_data = {
            "item_inventory_number": "TEST002",
            "name": "Test Product 2"
        }
        create_response = client.post("/api/products", json=product_data)
        assert create_response.status_code == 200
        
        # Then get it by ID
        product_id = create_response.json()["id"]
        response = client.get(f"/api/products/{product_id}")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == product_id

class TestInventoryAPI:
    """Test inventory API endpoints"""
    
    def test_get_inventory(self):
        """Test getting all inventory items"""
        response = client.get("/api/inventory")
        assert response.status_code == 200
        inventory = response.json()
        assert isinstance(inventory, list)
        if inventory:  # If there are inventory items
            assert "id" in inventory[0]
            assert "product_id" in inventory[0]
            assert "quantity" in inventory[0]
    
    def test_create_inventory_item(self):
        """Test creating a new inventory item"""
        inventory_data = {
            "product_id": "test-product-id",
            "quantity": 10,
            "purchase_price": 25.00,
            "list_price": 45.00
        }
        response = client.post("/api/inventory", json=inventory_data)
        assert response.status_code == 200
        inventory = response.json()
        assert inventory["quantity"] == 10
        assert inventory["purchase_price"] == 25.00
        assert "id" in inventory

class TestSalesAPI:
    """Test sales API endpoints"""
    
    def test_get_sales(self):
        """Test getting all sales"""
        response = client.get("/api/sales")
        assert response.status_code == 200
        sales = response.json()
        assert isinstance(sales, list)
        if sales:  # If there are sales
            assert "id" in sales[0]
            assert "product_id" in sales[0]
            assert "quantity_sold" in sales[0]
    
    def test_create_sale(self):
        """Test creating a new sale"""
        sale_data = {
            "product_id": "test-product-id",
            "quantity_sold": 1,
            "sell_price": 45.00
        }
        response = client.post("/api/sales", json=sale_data)
        assert response.status_code == 200
        sale = response.json()
        assert sale["quantity_sold"] == 1
        assert sale["sell_price"] == 45.00
        assert "id" in sale

class TestAnalyticsAPI:
    """Test analytics API endpoints"""
    
    def test_get_top_products(self):
        """Test getting top products analytics"""
        response = client.get("/api/analytics/top-products")
        assert response.status_code == 200
        data = response.json()
        assert "top_by_revenue" in data
        assert "top_by_margin" in data
        assert isinstance(data["top_by_revenue"], list)
        assert isinstance(data["top_by_margin"], list)
    
    def test_get_profit_analysis(self):
        """Test getting profit analysis"""
        response = client.get("/api/analytics/profit-analysis")
        assert response.status_code == 200
        data = response.json()
        assert "by_brand" in data
        assert "by_category" in data
        assert isinstance(data["by_brand"], list)
        assert isinstance(data["by_category"], list)

class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_product_data(self):
        """Test creating product with invalid data"""
        invalid_data = {
            "name": "Test Product"  # Missing required item_inventory_number
        }
        response = client.post("/api/products", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_inventory_data(self):
        """Test creating inventory with invalid data"""
        invalid_data = {
            "quantity": "invalid"  # Should be integer
        }
        response = client.post("/api/inventory", json=invalid_data)
        assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 