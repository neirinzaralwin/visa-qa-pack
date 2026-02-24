# Deployment Guide

## Railway Issues
Railway is having persistent 502 errors despite multiple approaches:
- ❌ Nixpacks build
- ❌ Docker build  
- ❌ Flat structure
- ❌ Minimal app

## Recommended: Deploy to Render

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: visa-qa-pack-api
   - **Root Directory**: `.` (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free

### Step 3: Environment Variables
Add these in Render dashboard:
- `GOOGLE_AI_API_KEY`: Your Google AI API key
- `FIREBASE_PROJECT_ID`: Your Firebase project ID
- `FIREBASE_PRIVATE_KEY`: Your Firebase private key
- `FIREBASE_CLIENT_EMAIL`: Your Firebase client email

### Step 4: Deploy
- Click "Create Web Service"
- Wait for deployment (2-3 minutes)
- Test at: `https://your-app-name.onrender.com/health`

## Alternative: Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Configure as Python API

## Current Working Endpoints
Once deployed, these endpoints will work:
- `GET /health` - Health check
- `POST /api/chat` - Simple chat
- `POST /api/generate-reply` - Advanced chat
- `GET /api/prompt` - Get AI prompt
- `PUT /api/prompt` - Update AI prompt

## Frontend Integration
Set `NEXT_PUBLIC_API_URL` to your deployed API URL.
