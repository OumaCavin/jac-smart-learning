#!/bin/bash

# Start Frontend Service Script
# React frontend development server startup script

set -e

echo "🎨 Starting JAC Smart Learning Frontend..."

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found. Make sure you're in the project root."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | sed 's/v//')
REQUIRED_VERSION="16.0.0"

if ! npx semver -r ">=$REQUIRED_VERSION" "$NODE_VERSION" &>/dev/null; then
    echo "⚠️  Node.js version $NODE_VERSION detected. Version $REQUIRED_VERSION+ is recommended."
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

# Set environment variables
export REACT_APP_API_URL="${REACT_APP_API_URL:-http://localhost:8000}"
export REACT_APP_WS_URL="${REACT_APP_WS_URL:-ws://localhost:8000}"
export REACT_APP_NODE_ENV="${REACT_APP_NODE_ENV:-development}"

# Check if .env file exists in frontend directory
if [ -f "frontend/.env" ]; then
    echo "📄 Loading frontend environment variables from frontend/.env..."
    export $(grep -v '^#' frontend/.env | xargs)
fi

echo "🔧 Frontend Configuration:"
echo "   - API URL: $REACT_APP_API_URL"
echo "   - WebSocket URL: $REACT_APP_WS_URL"
echo "   - Node Environment: $REACT_APP_NODE_ENV"

# Navigate to frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🚀 Starting React development server..."
echo "   Frontend: http://localhost:3000"
echo "   API: $REACT_APP_API_URL"
echo ""

# Start React development server
npm start

echo "✅ Frontend development server stopped"