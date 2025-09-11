#!/bin/bash

# Test script for Docker setup verification
# This script helps verify that the Docker setup works correctly

echo "🧪 Testing Docker Setup for Portfolio Analyzer"
echo "=============================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Please copy env.example to .env and configure your database credentials"
    exit 1
fi

echo "✅ .env file found"

# Check if required environment variables are set
source .env

required_vars=("DB_ROOT_PASSWORD" "DB_USER" "DB_PASSWORD" "DB_NAME" "SECRET_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "❌ Missing required environment variables:"
    for var in "${missing_vars[@]}"; do
        echo "   - $var"
    done
    echo "   Please update your .env file with the required values"
    exit 1
fi

echo "✅ All required environment variables are set"

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null || true

# Build and start the containers
echo "🚀 Building and starting containers..."
if docker-compose up --build -d; then
    echo "✅ Containers started successfully"
else
    echo "❌ Failed to start containers"
    exit 1
fi

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
timeout=300  # 5 minutes
elapsed=0

while [ $elapsed -lt $timeout ]; do
    if docker-compose ps | grep -q "healthy"; then
        echo "✅ Services are healthy"
        break
    fi
    
    echo "   Still waiting... (${elapsed}s elapsed)"
    sleep 10
    elapsed=$((elapsed + 10))
done

if [ $elapsed -ge $timeout ]; then
    echo "❌ Services did not become healthy within ${timeout} seconds"
    echo "📋 Container status:"
    docker-compose ps
    echo "📋 Container logs:"
    docker-compose logs --tail=50
    exit 1
fi

# Test web application
echo "🌐 Testing web application..."
if curl -f -s http://localhost:5000 > /dev/null; then
    echo "✅ Web application is responding"
else
    echo "❌ Web application is not responding"
    echo "📋 Web container logs:"
    docker-compose logs web --tail=20
    exit 1
fi

echo ""
echo "🎉 Docker setup test completed successfully!"
echo "🌐 Your application is available at: http://localhost:5000"
echo "🔑 Admin credentials:"
echo "   Username: admin"
echo "   Password: [from your .env ADMIN_PASSWORD]"
echo ""
echo "📋 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
