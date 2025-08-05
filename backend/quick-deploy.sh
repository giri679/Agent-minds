#!/bin/bash

# AI Education Agent - Quick Deployment Script
# One-click deployment for production

echo "🚀 AI Education Agent - Quick Deploy"
echo "===================================="
echo ""

# Check if running on Windows (Git Bash/WSL)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "⚠️  Detected Windows environment"
    echo "For Windows deployment, please use Docker Desktop"
    echo ""
    echo "Quick Windows Setup:"
    echo "1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/"
    echo "2. Open PowerShell as Administrator"
    echo "3. Run: docker-compose up -d"
    echo ""
    read -p "Press Enter to continue with current setup..."
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker not found."
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

echo "✅ Docker found"

# Setup environment
echo "⚙️  Setting up environment..."

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# AI Education Agent Environment Configuration
OPENAI_API_KEY=AIzaSyDhQduSfCjBzsEAUNwjEXTfSXon2gqkUMs
DATABASE_URL=postgresql://ai_user:ai_password@postgres:5432/ai_education
REDIS_URL=redis://redis:6379
SECRET_KEY=ai_education_secret_key_2024_production
JWT_SECRET_KEY=jwt_secret_key_for_ai_education_2024
ENVIRONMENT=production
DEBUG=false
NEXT_PUBLIC_API_URL=http://localhost:8000
DEFAULT_MODEL=gpt-4
FALLBACK_MODEL=gpt-3.5-turbo
EOF
    echo "✅ Environment file created"
else
    echo "✅ Environment file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs backups uploads
echo "✅ Directories created"

# Deploy the application
echo ""
echo "🚀 Deploying AI Education Agent..."
echo "This may take a few minutes..."
echo ""

# Stop any existing containers
docker-compose down 2>/dev/null || true

# Pull and start services
if docker-compose up -d; then
    echo ""
    echo "⏳ Waiting for services to start..."
    sleep 30

    # Check if services are running
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo ""
        echo "🎉 SUCCESS! AI Education Agent is now running!"
        echo ""
        echo "🌐 Access your AI Education Agent:"
        echo "   📚 API: http://localhost:8000"
        echo "   📖 API Documentation: http://localhost:8000/docs"
        echo "   🔍 Health Check: http://localhost:8000/health"
        echo ""
        echo "🧪 Test the AI features:"
        echo "   curl http://localhost:8000/"
        echo "   curl http://localhost:8000/api/analytics/ai-insights/STU001"
        echo ""
        echo "📊 View logs:"
        echo "   docker-compose logs -f"
        echo ""
        echo "🛑 Stop services:"
        echo "   docker-compose down"
        echo ""
        echo "🎓 Your AI Education Agent is ready to transform learning!"

    else
        echo "❌ Services started but health check failed"
        echo "📋 Checking logs..."
        docker-compose logs backend
        exit 1
    fi
else
    echo "❌ Failed to start services"
    echo "📋 Checking logs..."
    docker-compose logs
    exit 1
fi