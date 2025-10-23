#!/bin/bash

# Garagefy Render Deployment Helper
# This script helps verify everything is ready for deployment

echo "🚀 Garagefy Render Deployment Helper"
echo "===================================="
echo ""

# Check if backend/.env exists
if [ -f "backend/.env" ]; then
    echo "✅ backend/.env file found"
    
    # Check for required environment variables
    echo ""
    echo "📋 Checking environment variables..."
    
    required_vars=("AIRTABLE_API_KEY" "AIRTABLE_BASE_ID" "MS_CLIENT_ID" "MS_CLIENT_SECRET" "MS_TENANT_ID" "CLOUDINARY_API_KEY" "CLOUDINARY_API_SECRET")
    
    for var in "${required_vars[@]}"; do
        if grep -q "^${var}=" backend/.env; then
            echo "  ✅ $var is set"
        else
            echo "  ❌ $var is MISSING"
        fi
    done
else
    echo "❌ backend/.env file not found!"
    echo "   Please create it from backend/.env.example"
    exit 1
fi

echo ""
echo "📦 Checking deployment files..."

# Check render.yaml
if [ -f "render.yaml" ]; then
    echo "  ✅ render.yaml exists"
else
    echo "  ❌ render.yaml missing"
fi

# Check requirements.txt
if [ -f "backend/requirements.txt" ]; then
    echo "  ✅ backend/requirements.txt exists"
else
    echo "  ❌ backend/requirements.txt missing"
fi

echo ""
echo "🔍 Checking Git status..."
git_status=$(git status --porcelain)
if [ -z "$git_status" ]; then
    echo "  ✅ All changes committed"
else
    echo "  ⚠️  Uncommitted changes detected"
    echo "     Run: git add . && git commit -m 'Ready for deployment' && git push"
fi

echo ""
echo "📊 Current branch:"
current_branch=$(git branch --show-current)
echo "  Branch: $current_branch"

echo ""
echo "=================================="
echo "✨ Ready for Render Deployment!"
echo "=================================="
echo ""
echo "📝 Next Steps (Manual - I'll guide you):"
echo ""
echo "1️⃣  Open your browser and go to:"
echo "    👉 https://render.com"
echo ""
echo "2️⃣  Click 'Get Started for Free'"
echo "    - Sign up with GitHub (alwahis)"
echo ""
echo "3️⃣  Click 'New +' → 'Web Service'"
echo "    - Connect repository: alwahis/Garagefy"
echo "    - Branch: $current_branch"
echo ""
echo "4️⃣  Render will auto-detect settings from render.yaml ✅"
echo ""
echo "5️⃣  Click 'Advanced' and add these environment variables:"
echo ""
echo "    Copy from backend/.env:"
echo "    -------------------------"

# Display environment variables (masked)
if [ -f "backend/.env" ]; then
    echo "    AIRTABLE_API_KEY=$(grep '^AIRTABLE_API_KEY=' backend/.env | cut -d'=' -f2 | head -c 20)..."
    echo "    AIRTABLE_BASE_ID=$(grep '^AIRTABLE_BASE_ID=' backend/.env | cut -d'=' -f2)"
    echo "    MS_CLIENT_ID=$(grep '^MS_CLIENT_ID=' backend/.env | cut -d'=' -f2 | head -c 20)..."
    echo "    MS_CLIENT_SECRET=$(grep '^MS_CLIENT_SECRET=' backend/.env | cut -d'=' -f2 | head -c 20)..."
    echo "    MS_TENANT_ID=$(grep '^MS_TENANT_ID=' backend/.env | cut -d'=' -f2)"
    echo "    EMAIL_ADDRESS=$(grep '^EMAIL_ADDRESS=' backend/.env | cut -d'=' -f2)"
    echo "    CLOUDINARY_CLOUD_NAME=$(grep '^CLOUDINARY_CLOUD_NAME=' backend/.env | cut -d'=' -f2)"
    echo "    CLOUDINARY_API_KEY=$(grep '^CLOUDINARY_API_KEY=' backend/.env | cut -d'=' -f2)"
    echo "    CLOUDINARY_API_SECRET=$(grep '^CLOUDINARY_API_SECRET=' backend/.env | cut -d'=' -f2 | head -c 20)..."
fi

echo ""
echo "6️⃣  Click 'Create Web Service' and wait 3-5 minutes"
echo ""
echo "7️⃣  Once deployed, copy your backend URL (e.g., https://garagefy-backend.onrender.com)"
echo ""
echo "8️⃣  Update Netlify:"
echo "    👉 https://app.netlify.com/sites/garagefy-app-8zts3/settings/deploys"
echo "    - Add variable: REACT_APP_API_URL = <your-render-url>"
echo "    - Trigger redeploy"
echo ""
echo "9️⃣  Test: Visit https://garagefy.app"
echo ""
echo "=================================="
echo "💡 Need help? Check RENDER_DEPLOYMENT.md"
echo "=================================="
