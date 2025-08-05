@echo off
REM AI Education Agent - Windows Deployment Script

echo 🚀 AI Education Agent - Windows Deployment
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo After installation, restart your computer and run this script again.
    pause
    exit /b 1
)

echo ✅ Docker found

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose not found!
    echo Please make sure Docker Desktop is properly installed.
    pause
    exit /b 1
)

echo ✅ Docker Compose found

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    (
        echo # AI Education Agent Environment Configuration
        echo OPENAI_API_KEY=AIzaSyDhQduSfCjBzsEAUNwjEXTfSXon2gqkUMs
        echo DATABASE_URL=postgresql://ai_user:ai_password@postgres:5432/ai_education
        echo REDIS_URL=redis://redis:6379
        echo SECRET_KEY=ai_education_secret_key_2024_production
        echo JWT_SECRET_KEY=jwt_secret_key_for_ai_education_2024
        echo ENVIRONMENT=production
        echo DEBUG=false
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo DEFAULT_MODEL=gpt-4
        echo FALLBACK_MODEL=gpt-3.5-turbo
    ) > .env
    echo ✅ Environment file created
) else (
    echo ✅ Environment file already exists
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "uploads" mkdir uploads
echo ✅ Directories created

echo.
echo 🚀 Deploying AI Education Agent...
echo This may take a few minutes...
echo.

REM Stop any existing containers
docker-compose down >nul 2>&1

REM Start services
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ Failed to start services
    echo 📋 Checking logs...
    docker-compose logs
    pause
    exit /b 1
)

echo.
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo.
echo 🎉 SUCCESS! AI Education Agent is now running!
echo.
echo 🌐 Access your AI Education Agent:
echo    📚 API: http://localhost:8000
echo    📖 API Documentation: http://localhost:8000/docs
echo    🔍 Health Check: http://localhost:8000/health
echo.
echo 🧪 Test the AI features:
echo    curl http://localhost:8000/
echo    curl http://localhost:8000/api/analytics/ai-insights/STU001
echo.
echo 📊 Management commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart: docker-compose restart
echo.
echo 🎓 Your AI Education Agent is ready to transform learning!
echo.

REM Open browser to API documentation
start http://localhost:8000/docs

pause