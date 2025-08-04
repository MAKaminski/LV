#!/bin/bash

# LV Project Local Services Stop Script
# This script stops services started without Docker

set -e

echo "🛑 LV Project Local Services Stop"
echo "=================================="

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
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Stop Backend
echo "🐍 Stopping FastAPI Backend..."
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        print_status 0 "Backend stopped (PID: $BACKEND_PID)"
    else
        print_warning "Backend process not found (PID: $BACKEND_PID)"
    fi
    rm -f backend.pid
else
    print_warning "Backend PID file not found"
fi

# Stop Frontend
echo "⚛️  Stopping React Frontend..."
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        print_status 0 "Frontend stopped (PID: $FRONTEND_PID)"
    else
        print_warning "Frontend process not found (PID: $FRONTEND_PID)"
    fi
    rm -f frontend.pid
else
    print_warning "Frontend PID file not found"
fi

# Kill any remaining processes on the ports
echo "🔍 Cleaning up port processes..."
BACKEND_PROCESSES=$(lsof -ti:8000 2>/dev/null || true)
FRONTEND_PROCESSES=$(lsof -ti:3000 2>/dev/null || true)

if [ ! -z "$BACKEND_PROCESSES" ]; then
    echo "Killing processes on port 8000: $BACKEND_PROCESSES"
    kill -9 $BACKEND_PROCESSES
    print_status 0 "Backend port 8000 cleared"
fi

if [ ! -z "$FRONTEND_PROCESSES" ]; then
    echo "Killing processes on port 3000: $FRONTEND_PROCESSES"
    kill -9 $FRONTEND_PROCESSES
    print_status 0 "Frontend port 3000 cleared"
fi

echo ""
echo "🎉 All services stopped successfully!"
echo "====================================" 