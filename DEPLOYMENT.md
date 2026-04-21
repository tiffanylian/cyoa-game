# Deployment Guide

Your Flask app is ready to deploy! Here are the easiest options:

## Option 1: Railway (Recommended - Free Credits)

1. **Sign up** at [railway.app](https://railway.app) (free with GitHub)

2. **Connect your repository**:
   - Create a GitHub repo: `git init && git add . && git commit -m "initial commit" && git remote add origin <your-repo-url>`
   - Push to GitHub: `git push -u origin main`
   - Go to Railway → New Project → Import from GitHub → Select your repo

3. **Set Environment Variables** in Railway:
   - Go to Variables
   - Add `OPENAI_API_KEY=<your-api-key>`
   - Add `FLASK_ENV=production`

4. **Deploy**: Click "Deploy" - Railway auto-deploys and gives you a public URL

## Option 2: Render (Free Tier Available)

1. **Sign up** at [render.com](https://render.com) (free GitHub signup)

2. **Create new Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub repo
   - Environment: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn web_app:app`

3. **Set Environment Variables**:
   - In Service Settings → Environment
   - Add `OPENAI_API_KEY=<your-api-key>`

4. **Deploy**: Click "Create Web Service" - Render builds and deploys

## Option 3: PythonAnywhere (Simple, Free Tier)

1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)

2. **Upload your code**:
   - Download your project as ZIP
   - Use "Upload a file" in PythonAnywhere
   - Extract the ZIP

3. **Create Web App**:
   - Web tab → Add new web app
   - Choose Flask + Python 3.10
   - Set WSGI config to point to `web_app.py`

4. **Add API Key**:
   - Web app settings → Environment variables
   - `OPENAI_API_KEY=<your-api-key>`

5. **Reload**: Reload the app and get your public URL

## Option 4: Replit (Fastest - No Setup)

1. **Go to** [replit.com](https://replit.com)

2. **Upload your code**:
   - Create new Repl → Import from GitHub OR upload files

3. **Run immediately**:
   - Click "Run"
   - Replit gives you a public URL automatically

4. **Set Secret** (for API key):
   - Tools → Secrets
   - Add `OPENAI_API_KEY`

## Get Your OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (you can only see it once!)
5. Add it to your hosting platform's environment variables

## Testing Before Deploying

To test locally with production settings:

```bash
source venv/bin/activate
pip install gunicorn
gunicorn web_app:app --bind 0.0.0.0:5000
```

Then visit `http://localhost:5000`

## Which Platform Should I Choose?

- **Railway**: Best balance - free credits, easy setup, great performance
- **Render**: Reliable free tier, good support
- **PythonAnywhere**: Simplest for beginners, free tier works
- **Replit**: Fastest to get online, best for quick sharing

**Recommended: Start with Railway** - it's the most developer-friendly and has generous free credits ($5/month for new users).
