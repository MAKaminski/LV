#!/bin/bash

# LV Project Health Check Script
# This script verifies that all services are running and healthy

set -e

echo "🔍 LV Project Health Check"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Docker is running
echo "🐳 Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    print_status 1 "Docker is not running"
else
    print_status 0 "Docker is running"
fi

# Check if Docker Compose is available
echo "📦 Checking Docker Compose..."
if ! docker-compose --version > /dev/null 2>&1; then
    print_status 1 "Docker Compose is not available"
else
    print_status 0 "Docker Compose is available"
fi

# Check if services are running
echo "🚀 Checking service status..."
if ! docker-compose -f docker/docker-compose.yml ps | grep -q "Up"; then
    print_warning "Services are not running. Starting services..."
    docker-compose -f docker/docker-compose.yml up -d
    sleep 10
fi

# Check PostgreSQL
echo "🗄️  Checking PostgreSQL..."
if docker exec lv_postgres pg_isready -U postgres > /dev/null 2>&1; then
    print_status 0 "PostgreSQL is healthy"
else
    print_status 1 "PostgreSQL is not responding"
fi

# Check FastAPI Backend
echo "🐍 Checking FastAPI Backend..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status 0 "FastAPI Backend is healthy"
else
    print_status 1 "FastAPI Backend is not responding"
fi

# Check React Frontend
echo "⚛️  Checking React Frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_status 0 "React Frontend is healthy"
else
    print_status 1 "React Frontend is not responding"
fi

# Check API endpoints
echo "🔗 Checking API endpoints..."
ENDPOINTS=(
    "http://localhost:8000/"
    "http://localhost:8000/health"
    "http://localhost:8000/api/products"
    "http://localhost:8000/api/inventory"
    "http://localhost:8000/api/sales"
    "http://localhost:8000/api/analytics/top-products"
    "http://localhost:8000/api/analytics/profit-analysis"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if curl -f "$endpoint" > /dev/null 2>&1; then
        print_status 0 "API endpoint $endpoint is responding"
    else
        print_status 1 "API endpoint $endpoint is not responding"
    fi
done

# Check database connectivity
echo "🔌 Checking database connectivity..."
if docker exec lv_postgres psql -U postgres -d lv_project -c "SELECT 1;" > /dev/null 2>&1; then
    print_status 0 "Database connectivity is working"
else
    print_status 1 "Database connectivity failed"
fi

# Check database schema
echo "📊 Checking database schema..."
TABLES=("products" "categories" "brands" "inventory" "sales" "orders" "order_items" "platform_goals" "admin_costs" "users")

for table in "${TABLES[@]}"; do
    if docker exec lv_postgres psql -U postgres -d lv_project -c "SELECT 1 FROM $table LIMIT 1;" > /dev/null 2>&1; then
        print_status 0 "Table $table exists"
    else
        print_status 1 "Table $table does not exist"
    fi
done

# Check environment variables
echo "🔧 Checking environment variables..."
if [ -f ".env" ]; then
    print_status 0 "Environment file (.env) exists"
else
    print_warning "Environment file (.env) not found. Using defaults."
fi

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
if python3 -c "import fastapi, psycopg2, pandas" > /dev/null 2>&1; then
    print_status 0 "Python dependencies are installed"
else
    print_warning "Some Python dependencies may be missing"
fi

# Check Node.js dependencies
echo "📦 Checking Node.js dependencies..."
if [ -d "src/frontend/node_modules" ]; then
    print_status 0 "Node.js dependencies are installed"
else
    print_warning "Node.js dependencies not found. Run 'npm install' in src/frontend/"
fi

# Performance checks
echo "⚡ Checking performance..."
BACKEND_RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" http://localhost:8000/health)
if (( $(echo "$BACKEND_RESPONSE_TIME < 1.0" | bc -l) )); then
    print_status 0 "Backend response time: ${BACKEND_RESPONSE_TIME}s (good)"
else
    print_warning "Backend response time: ${BACKEND_RESPONSE_TIME}s (slow)"
fi

# Memory usage check
echo "💾 Checking memory usage..."
MEMORY_USAGE=$(docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}" | grep lv_)
if [ ! -z "$MEMORY_USAGE" ]; then
    print_status 0 "Memory usage check completed"
    echo "$MEMORY_USAGE"
else
    print_warning "Could not retrieve memory usage"
fi

echo ""
echo "🎉 Health check completed!"
echo "=========================="

# Summary
echo "📋 Summary:"
echo "- Docker: ✅"
echo "- PostgreSQL: ✅"
echo "- FastAPI Backend: ✅"
echo "- React Frontend: ✅"
echo "- API Endpoints: ✅"
echo "- Database Schema: ✅"

echo ""
echo "🚀 All services are healthy and ready for development!" 