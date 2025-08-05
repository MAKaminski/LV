# LV Project - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LV Project System                           │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript)                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Dashboard     │  │   Inventory     │  │    Products     │ │
│  │   Analytics     │  │   Management    │  │   Management    │ │
│  │   Charts        │  │   Forms         │  │   CRUD          │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Backend (FastAPI + Python)                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   API Routes    │  │   Business      │  │   Data          │ │
│  │   CRUD Ops      │  │   Logic         │  │   Validation    │ │
│  │   Analytics     │  │   Calculations  │  │   & Migration   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Database (PostgreSQL)                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Products      │  │   Inventory     │  │     Sales       │ │
│  │   Categories    │  │   Orders        │  │   Platform      │ │
│  │   Brands        │  │   Users         │  │   Goals         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  External Integrations                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Excel Data    │  │   NIA AI       │  │   Docker        │ │
│  │   Migration     │  │   Integration   │  │   Deployment    │ │
│  │   Analysis      │  │   Context       │  │   Container     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

```
Excel File → Analysis → Migration → PostgreSQL → FastAPI → React → Dashboard
     ↓           ↓          ↓           ↓         ↓        ↓        ↓
  LaceLuxx   Structure   Normalized   Queries   API      UI      Analytics
  Inventory   Detection   Schema       & Index   Endpoints Charts  & Reports
```

## 🗄️ Database Architecture

### Core Entities Relationship
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Categories │    │   Products  │    │   Brands    │
│             │    │             │    │             │
│ - id        │◄───┤ - category_id│    │ - id        │
│ - name      │    │ - brand_id  │───►│ - name      │
│ - description│   │ - name      │    │ - description│
└─────────────┘    │ - sku       │    └─────────────┘
                   │ - description│
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Inventory  │
                   │             │
                   │ - product_id│
                   │ - quantity  │
                   │ - prices    │
                   │ - status    │
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐    ┌─────────────┐
                   │    Sales    │    │   Orders    │
                   │             │    │             │
                   │ - product_id│    │ - order_id  │
                   │ - quantity  │    │ - buyer_id  │
                   │ - revenue   │    │ - seller_id │
                   │ - profit    │    │ - total     │
                   └─────────────┘    └─────────────┘
```

## 🎯 API Architecture

### RESTful Endpoints Structure
```
/api/
├── products/
│   ├── GET /           # List all products
│   ├── POST /          # Create product
│   └── GET /{id}       # Get specific product
├── inventory/
│   ├── GET /           # List inventory
│   ├── POST /          # Add inventory item
│   └── PUT /{id}       # Update inventory
├── sales/
│   ├── GET /           # List sales
│   ├── POST /          # Record sale
│   └── GET /analytics  # Sales analytics
└── analytics/
    ├── GET /top-products    # Top products
    └── GET /profit-analysis # Profit analysis
```

## 🐳 Deployment Architecture

### Docker Container Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Frontend   │  │   Backend   │  │ PostgreSQL  │        │
│  │  React App  │  │  FastAPI    │  │  Database   │        │
│  │  Port:3000  │  │  Port:8000  │  │  Port:5432  │        │
│  │             │  │             │  │             │        │
│  │ - TypeScript│  │ - Python    │  │ - Schema    │        │
│  │ - Recharts  │  │ - SQLAlchemy│  │ - Data      │        │
│  │ - Axios     │  │ - Pydantic  │  │ - Indexes   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 🔐 Security Architecture

### Authentication & Authorization
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Database      │
│                 │    │                 │    │                 │
│ - Form Validation│   │ - CORS Middleware│   │ - Row Level     │
│ - Input Sanitize│   │ - JWT Tokens    │   │   Security      │
│ - HTTPS         │   │ - Rate Limiting │   │ - Prepared      │
│                 │    │                 │   │   Statements    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Analytics Architecture

### Data Processing Pipeline
```
Raw Data → ETL → Normalized DB → Analytics Engine → Visualization
   ↓         ↓         ↓              ↓              ↓
Excel    Migration  PostgreSQL    FastAPI        React
Files    Scripts    Schema        Queries       Charts
```

## 🔄 State Management Architecture

### Frontend State Flow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   React     │    │   FastAPI   │
│   Action    │───►│   State     │───►│   Backend   │
│             │    │             │    │             │
│ - Form Input│    │ - useState  │    │ - Database  │
│ - Button    │    │ - useEffect │    │ - Business  │
│ - Navigation│    │ - Context   │    │   Logic     │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Performance Architecture

### Optimization Strategies
1. **Database**: Indexed queries, connection pooling
2. **Backend**: Async operations, caching
3. **Frontend**: Lazy loading, memoization
4. **Deployment**: Container orchestration, load balancing

## 🔧 Development Architecture

### Feature-Driven Development
```
Feature X → Analysis → Design → Implementation → Testing → Deployment
    ↓         ↓        ↓           ↓            ↓         ↓
  MEGA_PROMPT  ERD    Schema    Code        Tests    Docker
  Specs        Design  Migration Components  Coverage  Compose
```

## 📈 Scalability Architecture

### Horizontal Scaling
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Load      │    │   Multiple  │    │   Database  │
│   Balancer  │───►│   Backend   │───►│   Replicas  │
│             │    │   Instances │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🔄 CI/CD Architecture

### Deployment Pipeline
```
Code → Tests → Build → Docker → Deploy → Monitor
  ↓      ↓      ↓       ↓        ↓        ↓
Git    Jest   Webpack  Images   Docker   Logs
Push   Tests  Bundle   Compose  Compose  Analytics
```

---

**Last Updated**: August 2024  
**Version**: 1.0.0  
**Maintainer**: LV Project Team 