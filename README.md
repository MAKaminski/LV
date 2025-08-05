# LV Project - Inventory Management System

A full-stack inventory management system designed to replace manual Excel-based operations with a modern, database-driven web application.

## 🚀 Features

### ✅ Feature 1: ERD + Schema Development
- **Normalized PostgreSQL database** with proper relationships
- **CSV data migration** from Platform Luxx Base Data
- **Audit trail** for all transactions
- **Performance optimized** with proper indexing

### ✅ Feature 2: Input Screen Replacement
- **React-based web interface** for data entry
- **CRUD operations** for products, inventory, and sales
- **Form validation** aligned with database schema
- **Real-time data synchronization**

### ✅ Feature 3: Analytics & Home Dashboard
- **Real-time analytics dashboard** with charts and graphs
- **Top selling products** analysis by revenue and margin
- **Profit analysis** by brand and category
- **Interactive visualizations** using Recharts

## 🏗️ Architecture

```
LV/
├── context/           # NIA context and project documentation
├── data/             # Data files and analysis results
│   └── inputs/       # CSV input files
├── docs/             # Project documentation
├── src/              # Application source code
│   ├── backend/      # FastAPI server
│   ├── database/     # Database schemas and migrations
│   └── frontend/     # React application
├── scripts/          # Data migration and analysis scripts
├── docker/           # Docker configuration
├── tests/            # Test suites
└── nia_index/        # NIA indexing tools
```

## 🛠️ Technology Stack

- **Frontend**: React with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Charts**: Recharts
- **Deployment**: Docker + Docker Compose
- **AI Integration**: NIA for development assistance

## 📊 Database Schema

The system uses a normalized database design optimized for CSV-based inventory data:

### Core Entities
- **Users**: Seller and buyer management (126 users)
- **Brands**: Luxury brand information (89 brands)
- **Products**: Core product information with brand relationships (60 products)
- **Inventory**: Current stock levels and pricing (60 records)
- **Sales**: Transaction history with profit tracking (29 sales)

### Data Migration
- **Source**: Platform Luxx Base Data.csv (774 records)
- **Brand Extraction**: Intelligent pattern matching for luxury brands
- **Data Quality**: Handles various money formats and data inconsistencies
- **Weekly Updates**: Automated migration scripts for regular updates

## 🚀 Quick Start

### Prerequisites
- PostgreSQL (local installation)
- Python 3.9+
- Node.js 16+

### 1. Clone and Setup
```bash
git clone <repository-url>
cd LV
```

### 2. Database Setup
```bash
# Create database
createdb lv_project

# Apply schema
psql -d lv_project -f src/database/schema.sql
```

### 3. Migrate CSV Data
```bash
# Install dependencies
pip install pandas psycopg2-binary python-dotenv

# Run migration
python3 scripts/simple_csv_migrate.py

# Extract brands (if needed)
python3 scripts/extract_brands.py
```

### 4. Start the Application
```bash
# Backend
cd src/backend && python3 main.py

# Frontend (in new terminal)
cd src/frontend && npm start
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📈 Analytics Dashboard

The dashboard provides real-time insights including:

- **Top Products by Revenue**: Bar chart showing highest revenue generators
- **Top Products by Margin**: Profit margin analysis
- **Profit by Brand**: Pie chart of brand performance
- **Summary Cards**: Total revenue, profit, and average margin

## 🔧 Development

### Feature-Driven Development
All commits follow the pattern: `feat(FEATURE X): <description>`

### Running Tests
```bash
# Backend tests
cd src/backend && python -m pytest

# Frontend tests
cd src/frontend && npm test
```

### Database Management
```bash
# Connect to database
psql -d lv_project

# View schema
\dt
```

## 📝 API Endpoints

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create new product
- `GET /api/products/{id}` - Get specific product

### Inventory
- `GET /api/inventory` - List inventory items
- `POST /api/inventory` - Create inventory item

### Sales
- `GET /api/sales` - List sales
- `POST /api/sales` - Create sale record

### Analytics
- `GET /api/analytics/top-products` - Top products analysis
- `GET /api/analytics/profit-analysis` - Profit analysis

## 🤖 NIA Integration

This project is fully integrated with NIA for AI-powered development assistance:

- **Context Documentation**: All project context stored in `/context/`
- **Feature Tracking**: Each feature documented with implementation details
- **Code Analysis**: NIA can analyze and suggest improvements
- **Development Guidance**: AI assistance for implementation decisions

## 📊 Data Migration

The system includes comprehensive CSV data migration:

1. **Analysis**: `scripts/analyze_excel.py` analyzes the CSV structure
2. **Migration**: `scripts/simple_csv_migrate.py` converts data to PostgreSQL
3. **Brand Extraction**: `scripts/extract_brands.py` extracts brands from product names
4. **Validation**: Data integrity checks and error handling
5. **Weekly Updates**: `scripts/weekly_update.py` for routine data updates

## 🎯 Success Metrics

- ✅ **CSV Migration**: Complete migration from Platform Luxx Base Data
- ✅ **Real-time Analytics**: Automated dashboard replacing manual analysis
- ✅ **Scalable Architecture**: Normalized database supporting growth
- ✅ **Feature-Driven Development**: Atomic commits with clear traceability
- ✅ **AI Integration**: NIA-powered development assistance
- ✅ **Database Cleanup**: Removed unnecessary tables, optimized for CSV data

## 🔮 Future Enhancements

- **Multi-platform Integration**: Direct API connections to Poshmark, Whatnot
- **Advanced Analytics**: Machine learning for price optimization
- **Mobile App**: React Native mobile application
- **Automated Reporting**: Scheduled reports and alerts
- **Inventory Forecasting**: Predictive analytics for stock management

---

**Built with ❤️ using Feature-Driven Development and AI-powered assistance**