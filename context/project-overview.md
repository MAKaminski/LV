# LV Project - Context Overview

## Project Summary
The LV Project is a full-stack inventory management system designed to replace manual Excel-based operations with a modern, database-driven web application.

## Core Objectives
- Convert Excel-based inventory management to a PostgreSQL database system
- Create React-based web interface for data entry and management
- Implement real-time analytics dashboard
- Maintain feature-driven development with atomic commits

## Technology Stack
- **Frontend**: React with TypeScript
- **Backend**: FastAPI (Python) or Node.js
- **Database**: PostgreSQL
- **Deployment**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **AI Integration**: NIA for code analysis and development assistance

## Feature Roadmap

### Feature 1: ERD + Schema Development
- Parse existing Excel data to identify entities and relationships
- Design normalized ERD for inventory management
- Create PostgreSQL schema with proper relationships
- Implement data migration from Excel to database

### Feature 2: Input Screen Replacement
- React-based web interface for data entry
- CRUD operations for purchases, inventory, and sales
- Form validation aligned with database schema
- Real-time data synchronization

### Feature 3: Analytics & Home Dashboard
- Real-time analytics dashboard
- Top selling products analysis
- Buy vs sell price comparisons
- Revenue and margin tracking
- Interactive charts and filters

## Development Standards
- **Commit Convention**: `feat(FEATURE X): <description>`
- **Documentation**: Auto-generated README updates per feature
- **Testing**: Unit tests for all API endpoints
- **Deployment**: Docker containerization with CI/CD pipeline

## Current Status
- ✅ Project specification and documentation complete
- ✅ NIA integration established
- 🔄 Feature 1: ERD + Schema Development (In Progress)
- ⏳ Feature 2: Input Screen Replacement (Pending)
- ⏳ Feature 3: Analytics & Home Dashboard (Pending)

## Directory Structure
```
LV/
├── context/           # NIA context and project documentation
├── docs/             # Project documentation and specifications
├── src/              # Application source code
│   ├── frontend/     # React application
│   ├── backend/      # FastAPI/Node.js server
│   └── database/     # Database schemas and migrations
├── nia_index/        # NIA indexing tools
├── tests/            # Test suites
├── docker/           # Docker configuration
└── scripts/          # Development and deployment scripts
``` 