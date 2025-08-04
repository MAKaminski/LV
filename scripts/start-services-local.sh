#!/bin/bash

# LV Project Local Services Startup Script
# This script starts services without Docker for development

set -e

echo "🚀 LV Project Local Services Startup"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "docs/MEGA_PROMPT.md" ]; then
    print_status 1 "Please run this script from the LV project root directory"
fi

print_info "Starting services without Docker..."

# Check Python dependencies
echo ""
echo "🐍 Checking Python dependencies..."
if python3 -c "import fastapi, uvicorn, sqlalchemy, psycopg2, pandas" 2>/dev/null; then
    print_status 0 "Python dependencies are installed"
else
    print_warning "Some Python dependencies may be missing"
    print_info "Installing Python dependencies..."
    pip3 install fastapi uvicorn sqlalchemy psycopg2-binary pandas python-dotenv
fi

# Check Node.js dependencies
echo ""
echo "📦 Checking Node.js dependencies..."
if [ -d "src/frontend/node_modules" ]; then
    print_status 0 "Node.js dependencies are installed"
else
    print_warning "Node.js dependencies not found"
    print_info "Installing Node.js dependencies..."
    cd src/frontend
    npm install
    cd ../..
fi

# Check if PostgreSQL is running locally
echo ""
echo "🗄️  Checking PostgreSQL..."
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    print_status 0 "PostgreSQL is running locally"
else
    print_warning "PostgreSQL not running locally"
    print_info "You may need to start PostgreSQL manually or install it"
    print_info "On macOS: brew install postgresql && brew services start postgresql"
    print_info "On Ubuntu: sudo apt-get install postgresql postgresql-contrib"
fi

# Start Backend
echo ""
echo "🐍 Starting FastAPI Backend..."
cd src/backend

# Check if backend is already running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status 0 "Backend is already running on http://localhost:8000"
else
    print_info "Starting backend server..."
    # Start backend in background
    python3 main.py &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../../backend.pid
    
    # Wait for backend to start
    sleep 3
    
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status 0 "Backend started successfully on http://localhost:8000"
    else
        print_status 1 "Backend failed to start"
    fi
fi
cd ../..

# Start Frontend
echo ""
echo "⚛️  Starting React Frontend..."
cd src/frontend

# Check if frontend is already running
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_status 0 "Frontend is already running on http://localhost:3000"
else
    print_info "Starting frontend server..."
    # Start frontend in background
    npm start &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../../frontend.pid
    
    # Wait for frontend to start
    sleep 10
    
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_status 0 "Frontend started successfully on http://localhost:3000"
    else
        print_status 1 "Frontend failed to start"
    fi
fi
cd ../..

# Health Check
echo ""
echo "🔍 Running health check..."
sleep 2

# Check all endpoints
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
        print_warning "API endpoint $endpoint is not responding"
    fi
done

# Final Summary
echo ""
echo "🎉 Services Started Successfully!"
echo "================================"
echo "✅ Backend: http://localhost:8000"
echo "✅ Frontend: http://localhost:3000"
echo "✅ API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Service PIDs saved to:"
echo "- Backend: backend.pid"
echo "- Frontend: frontend.pid"
echo ""
echo "🛑 To stop services:"
echo "- Backend: kill \$(cat backend.pid)"
echo "- Frontend: kill \$(cat frontend.pid)"
echo "- Or use: ./scripts/stop-services-local.sh" 