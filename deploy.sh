#!/bin/bash

echo "🚀 AI Education Agent - Vercel Deployment Script"
echo "================================================"

# Check if required files exist
echo "📋 Checking required files..."

if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found!"
    exit 1
fi

if [ ! -f "demo.html" ]; then
    echo "❌ demo.html not found!"
    exit 1
fi

if [ ! -f "package.json" ]; then
    echo "❌ package.json not found!"
    exit 1
fi

if [ ! -d "api" ]; then
    echo "❌ api directory not found!"
    exit 1
fi

echo "✅ All required files found!"

# Validate JSON files
echo "🔍 Validating configuration files..."

if ! node -e "JSON.parse(require('fs').readFileSync('vercel.json', 'utf8'))" 2>/dev/null; then
    echo "❌ vercel.json is not valid JSON!"
    exit 1
fi

if ! node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))" 2>/dev/null; then
    echo "❌ package.json is not valid JSON!"
    exit 1
fi

echo "✅ Configuration files are valid!"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "🚀 Starting deployment..."

# Deploy to Vercel
vercel --prod

echo "🎉 Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Check your Vercel dashboard for the deployment URL"
echo "2. Test all features on the live site"
echo "3. Share the URL with users!"
echo ""
echo "🔗 Your AI Education Agent is now live! ✨"
