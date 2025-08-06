# 🔧 Vercel Deployment Troubleshooting Guide

## 🚨 **Changes Not Reflecting? Here's How to Fix It:**

### **Step 1: Force Redeploy**

#### **Method A: Through Vercel Dashboard**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Find your project
3. Click on the latest deployment
4. Click **"Redeploy"** button
5. Wait for deployment to complete

#### **Method B: Using Git**
```bash
# Make a small change to trigger redeploy
echo "# Updated $(date)" >> README.md
git add .
git commit -m "Force redeploy - $(date)"
git push origin main
```

#### **Method C: Using Vercel CLI**
```bash
# Install Vercel CLI if not installed
npm install -g vercel

# Force production deployment
vercel --prod --force
```

### **Step 2: Clear Vercel Cache**

#### **Clear Build Cache:**
```bash
# Using Vercel CLI
vercel --prod --force --no-cache
```

#### **Or in Vercel Dashboard:**
1. Go to Project Settings
2. Click "Functions" tab
3. Click "Clear Cache"

### **Step 3: Verify Configuration**

#### **Check vercel.json syntax:**
```bash
# Validate JSON syntax
node -e "console.log('✅ Valid JSON:', JSON.parse(require('fs').readFileSync('vercel.json', 'utf8')))"
```

#### **Expected vercel.json structure:**
```json
{
  "buildCommand": "echo 'Building AI Education Agent...'",
  "outputDirectory": ".",
  "rewrites": [
    {"source": "/", "destination": "/demo.html"},
    {"source": "/api/(.*)", "destination": "/api/$1"}
  ],
  "functions": {
    "api/health.js": {"maxDuration": 10},
    "api/worksheets/ai-generate.js": {"maxDuration": 30}
  }
}
```

### **Step 4: Check File Structure**

#### **Required files in root:**
```
✅ demo.html (main app)
✅ vercel.json (config)
✅ package.json (metadata)
✅ api/ (directory with endpoints)
```

#### **Verify files exist:**
```bash
ls -la demo.html vercel.json package.json api/
```

### **Step 5: Test API Endpoints**

#### **Test after deployment:**
```bash
# Replace YOUR_DOMAIN with your actual Vercel URL
curl https://YOUR_DOMAIN.vercel.app/api/health
curl -X POST https://YOUR_DOMAIN.vercel.app/api/worksheets/ai-generate \
  -H "Content-Type: application/json" \
  -d '{"subject":"math","topic":"algebra"}'
```

## 🐛 **Common Issues & Solutions**

### **Issue 1: "404 - This page could not be found"**
**Solution:**
- Check if `demo.html` exists in root directory
- Verify `vercel.json` rewrites configuration
- Ensure no typos in file names

### **Issue 2: "API endpoints returning 404"**
**Solution:**
- Check if `api/` directory exists
- Verify API files have `.js` extension
- Check `vercel.json` functions configuration

### **Issue 3: "CORS errors in browser"**
**Solution:**
- Verify API files include CORS headers
- Check browser network tab for actual error
- Test API endpoints directly

### **Issue 4: "Build fails on Vercel"**
**Solution:**
- Check Vercel build logs
- Verify `package.json` syntax
- Ensure no missing dependencies

### **Issue 5: "Old version still showing"**
**Solution:**
- Clear browser cache (Ctrl+F5)
- Check if deployment actually completed
- Force redeploy using methods above

## 🔍 **Debugging Steps**

### **1. Check Deployment Status**
```bash
# Using Vercel CLI
vercel ls
vercel inspect YOUR_DEPLOYMENT_URL
```

### **2. View Build Logs**
1. Go to Vercel Dashboard
2. Click on your project
3. Click on latest deployment
4. Check "Build Logs" tab

### **3. Test Locally First**
```bash
# Test the same files locally
cd frontend
python -m http.server 3001
# Open http://localhost:3001/demo.html
```

### **4. Check Browser Console**
1. Open browser developer tools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

## 🚀 **Force Deployment Script**

Save this as `force-deploy.sh`:
```bash
#!/bin/bash
echo "🔄 Force redeploying AI Education Agent..."

# Update version to trigger change
npm version patch --no-git-tag-version

# Commit and push
git add .
git commit -m "Force redeploy - $(date)"
git push origin main

echo "✅ Deployment triggered! Check Vercel dashboard."
```

## 📞 **Still Having Issues?**

### **Quick Checklist:**
- [ ] Files committed to git repository
- [ ] vercel.json is valid JSON
- [ ] demo.html exists in root
- [ ] API directory exists with .js files
- [ ] Deployment completed successfully
- [ ] Browser cache cleared

### **Get Help:**
1. Check Vercel documentation
2. Review deployment logs
3. Test API endpoints individually
4. Verify all files are properly committed

**Your AI Education Agent should be working perfectly after following these steps! 🎓✨**
