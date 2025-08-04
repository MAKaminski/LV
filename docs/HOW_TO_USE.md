# LV Project - How to Use Guide

## 🚀 Quick Start Guide

### Prerequisites
- Docker and Docker Compose installed
- Python 3.9+ (for development)
- Node.js 16+ (for frontend development)
- Git for version control

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/MAKaminski/LV.git
cd LV

# Verify the structure
ls -la
```

### 2. Start the Application
```bash
# Start all services with Docker
docker-compose -f docker/docker-compose.yml up -d

# Check if services are running
docker-compose -f docker/docker-compose.yml ps
```

### 3. Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Using the Analytics Dashboard

### Dashboard Overview
The analytics dashboard provides real-time insights into your inventory management:

1. **Top Products by Revenue**: Bar chart showing highest revenue generators
2. **Top Products by Margin**: Profit margin analysis
3. **Profit by Brand**: Pie chart of brand performance
4. **Profit by Category**: Category-wise profit analysis
5. **Summary Cards**: Total revenue, profit, and average margin

### Interacting with Charts
- **Hover**: Get detailed information about data points
- **Click**: Select specific items for detailed analysis
- **Zoom**: Use mouse wheel to zoom in/out on charts
- **Legend**: Click legend items to show/hide data series

## 🔧 Development Workflow

### Using Cursor Debugger Commands

The project includes pre-configured debugger commands in `.vscode/launch.json`:

#### Quick Commands (F5 in Cursor)
1. **🚀 Start All Services (Docker)**: Launches all containers
2. **🐍 Debug FastAPI Backend**: Runs backend in debug mode
3. **📊 Debug Excel Analysis**: Analyzes Excel data structure
4. **🔄 Debug Data Migration**: Migrates Excel data to database
5. **🤖 Debug NIA Indexing**: Updates NIA repository index
6. **⚡ Debug Frontend (React)**: Runs React development server

#### Database Commands
- **🔍 Database: Connect to PostgreSQL**: Opens database shell
- **📊 Database: View Schema**: Shows table structure

#### Docker Commands
- **🐳 Docker: Start PostgreSQL**: Starts database only
- **🐳 Docker: Start Backend**: Starts API server only
- **🐳 Docker: Start Frontend**: Starts React app only
- **🐳 Docker: Stop All Services**: Stops all containers

### Manual Development Commands

#### Backend Development
```bash
# Navigate to backend
cd src/backend

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary

# Run development server
python3 main.py

# Access API docs
# http://localhost:8000/docs
```

#### Frontend Development
```bash
# Navigate to frontend
cd src/frontend

# Install dependencies
npm install

# Start development server
npm start

# Access application
# http://localhost:3000
```

#### Database Operations
```bash
# Connect to database
docker exec -it lv_postgres psql -U postgres -d lv_project

# View tables
\dt

# View data
SELECT * FROM products LIMIT 5;

# Exit database
\q
```

## 📊 Data Management

### Excel Data Migration

#### Step 1: Analyze Excel File
```bash
# Run Excel analysis
python3 scripts/analyze_excel.py

# This will:
# - Analyze the LaceLuxx Inventory Excel file
# - Generate structure report
# - Save analysis to data/excel_analysis.json
```

#### Step 2: Migrate Data to Database
```bash
# Run data migration
python3 scripts/migrate_excel_data.py

# This will:
# - Connect to PostgreSQL database
# - Migrate categories and brands
# - Migrate products and inventory
# - Migrate sales data
# - Provide migration summary
```

### Database Schema Management

#### View Current Schema
```bash
# Connect to database and view tables
docker exec -it lv_postgres psql -U postgres -d lv_project -c "\dt"

# View specific table structure
docker exec -it lv_postgres psql -U postgres -d lv_project -c "\d products"
```

#### Reset Database
```bash
# Stop containers
docker-compose -f docker/docker-compose.yml down

# Remove database volume
docker volume rm lv_postgres_data

# Restart containers
docker-compose -f docker/docker-compose.yml up -d
```

## 🔍 API Usage

### Products API
```bash
# Get all products
curl http://localhost:8000/api/products

# Create new product
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "item_inventory_number": "LV001",
    "name": "Sample Product",
    "description": "A sample product"
  }'

# Get specific product
curl http://localhost:8000/api/products/{product_id}
```

### Inventory API
```bash
# Get all inventory items
curl http://localhost:8000/api/inventory

# Add inventory item
curl -X POST http://localhost:8000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "uuid-here",
    "quantity": 10,
    "purchase_price": 25.00,
    "list_price": 45.00
  }'
```

### Analytics API
```bash
# Get top products
curl http://localhost:8000/api/analytics/top-products

# Get profit analysis
curl http://localhost:8000/api/analytics/profit-analysis
```

## 🧪 Testing

### Backend Testing
```bash
# Navigate to backend
cd src/backend

# Install pytest
pip install pytest

# Run tests
python -m pytest tests/ -v
```

### Frontend Testing
```bash
# Navigate to frontend
cd src/frontend

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 🔧 Configuration

### Environment Variables

#### Backend Configuration
```bash
# Database connection
DATABASE_URL=postgresql://postgres:password@localhost/lv_project

# API settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

#### Frontend Configuration
```bash
# API endpoint
REACT_APP_API_URL=http://localhost:8000

# Development settings
BROWSER=none
```

### Docker Configuration
```yaml
# docker/docker-compose.yml
services:
  postgres:
    environment:
      POSTGRES_DB: lv_project
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Docker Services Not Starting
```bash
# Check Docker status
docker --version
docker-compose --version

# Check if ports are in use
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Restart Docker
sudo systemctl restart docker
```

#### 2. Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check database logs
docker logs lv_postgres

# Reset database
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d
```

#### 3. Frontend Not Loading
```bash
# Check if React app is running
docker ps | grep frontend

# Check frontend logs
docker logs lv_frontend

# Rebuild frontend
docker-compose -f docker/docker-compose.yml build frontend
```

#### 4. API Not Responding
```bash
# Check if FastAPI is running
docker ps | grep backend

# Check backend logs
docker logs lv_backend

# Test API directly
curl http://localhost:8000/health
```

### Debug Mode

#### Backend Debug
```bash
# Run with debug logging
cd src/backend
uvicorn main:app --reload --log-level debug
```

#### Frontend Debug
```bash
# Run with debug logging
cd src/frontend
REACT_APP_DEBUG=true npm start
```

## 📈 Performance Optimization

### Database Optimization
```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM products WHERE category_id = 'uuid';

-- Add indexes for better performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_sales_date ON sales(date_sold);
```

### API Optimization
```python
# Enable caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Add rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
```

### Frontend Optimization
```javascript
// Enable React.memo for components
const ProductCard = React.memo(({ product }) => {
  return <div>{product.name}</div>
});

// Use React.lazy for code splitting
const Dashboard = React.lazy(() => import('./components/Dashboard'));
```

## 🔒 Security Best Practices

### Database Security
```sql
-- Create read-only user
CREATE USER readonly WITH PASSWORD 'password';
GRANT CONNECT ON DATABASE lv_project TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
```

### API Security
```python
# Add authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

# Add CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 Additional Resources

### Documentation
- **API Documentation**: http://localhost:8000/docs
- **Project README**: [README.md](README.md)
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Timeline**: [docs/TIMELINE.md](docs/TIMELINE.md)

### External Resources
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://reactjs.org/docs/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Docker Documentation**: https://docs.docker.com/

### Support
- **GitHub Issues**: Report bugs and feature requests
- **NIA Integration**: AI-powered development assistance
- **Project Context**: Check `/context/` directory for project details

---

**Last Updated**: August 4, 2024  
**Version**: 1.0.0  
**Maintainer**: LV Project Team 