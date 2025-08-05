#!/bin/bash

# AI Education Agent - Production Deployment Script
# This script deploys the AI Education Agent to production

set -e  # Exit on any error

echo "🚀 Starting AI Education Agent Production Deployment..."

# Configuration
PROJECT_NAME="ai-education-agent"
BACKUP_DIR="./backups"
LOG_FILE="./logs/deployment.log"

# Create necessary directories
mkdir -p logs backups uploads nginx/ssl monitoring

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
log "Checking prerequisites..."

if ! command_exists docker; then
    log "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    log "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

log "✅ Prerequisites check passed"

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    log "❌ .env.production file not found. Please create it with production settings."
    exit 1
fi

# Load environment variables
source .env.production

log "✅ Environment variables loaded"

# Pull latest images
log "📥 Pulling latest Docker images..."
docker-compose -f docker-compose.prod.yml pull

# Build application images
log "🔨 Building application images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Stop existing services
log "🛑 Stopping existing services..."
docker-compose -f docker-compose.prod.yml down

# Start services
log "🚀 Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
log "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
log "🔍 Checking service health..."
services=("postgres" "redis" "backend" "frontend")
for service in "${services[@]}"; do
    if docker-compose -f docker-compose.prod.yml ps $service | grep -q "Up"; then
        log "✅ $service is running"
    else
        log "❌ $service failed to start"
        docker-compose -f docker-compose.prod.yml logs $service
        exit 1
    fi
done

# Test API endpoints
log "🧪 Testing API endpoints..."
sleep 10

# Test health endpoint
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    log "✅ Backend API is responding"
else
    log "❌ Backend API is not responding"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

# Display deployment information
log "🎉 Deployment completed successfully!"
echo ""
echo "🌐 Access Points:"
echo "   📚 Frontend: http://localhost:3000"
echo "   🔧 Backend API: http://localhost:8000"
echo "   📖 API Docs: http://localhost:8000/docs"
echo "   🔍 Health Check: http://localhost:8000/health"
echo ""

log "✅ AI Education Agent is now running in production mode!"
log "📝 Check logs at: $LOG_FILE"