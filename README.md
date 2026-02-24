# Complete Chatbot Pack

A full-stack chatbot application with Flask API backend and Next.js frontend.

## Railway Deployment

### API Deployment
1. Push the `api/` directory to Railway
2. Railway will automatically detect the Python app
3. Uses Gunicorn as the WSGI server
4. Health check available at `/health`

### Frontend Deployment
1. Push the `frontend/` directory to Railway
2. Railway will automatically detect the Next.js app
3. Static files are served from the build output
4. Health check available at `/`

## Environment Variables

### API
- `GOOGLE_AI_API_KEY`: Google Generative AI API key
- `FIREBASE_CREDENTIALS`: Firebase service account JSON
- `DATABASE_URL`: Database connection URL

### Frontend
- `NEXT_PUBLIC_API_URL`: URL of the deployed API

## Local Development

### API
```bash
cd api
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
