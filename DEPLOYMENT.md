# Deployment Guide

This project can be deployed in multiple ways depending on your needs.

## Option 1: GitHub Pages (Static Version) ⭐ EASIEST

The static version (`docs/index.html`) runs entirely in the browser with no backend required.

### Setup GitHub Pages:

1. **Push your code to GitHub**
   ```bash
   git push origin claude/cafe-calorie-dollar-analyzer-SHDCV
   ```

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click Settings → Pages
   - Under "Source", select: `Deploy from a branch`
   - Under "Branch", select: `claude/cafe-calorie-dollar-analyzer-SHDCV` and `/docs`
   - Click Save

3. **Access your site**
   - Your site will be live at: `https://[username].github.io/laughing-system/`
   - It may take a few minutes for the first deployment

### Features of Static Version:
- ✅ Upload JSON files for analysis
- ✅ Interactive filtering by price and calories
- ✅ Beautiful responsive design
- ✅ Example data included
- ❌ No web scraping capability (browser limitation)
- ❌ No server-side processing

---

## Option 2: Render (Flask App) - FREE

Deploy the full Python Flask application with all features.

### Setup on Render:

1. **Sign up** at https://render.com (free tier available)

2. **Create a new Web Service**
   - Connect your GitHub repository
   - Select the branch: `claude/cafe-calorie-dollar-analyzer-SHDCV`

3. **Configure the service**
   - Name: `cafe-calorie-analyzer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

4. **Add gunicorn to requirements**
   Add this line to `requirements.txt`:
   ```
   gunicorn>=21.0.0
   ```

5. **Deploy**
   - Render will automatically deploy your app
   - You'll get a URL like: `https://cafe-calorie-analyzer.onrender.com`

### Features:
- ✅ Full Flask application
- ✅ All features including web scraping
- ✅ File uploads
- ✅ RESTful API
- ⚠️ Free tier may sleep after inactivity (slow first load)

---

## Option 3: PythonAnywhere - FREE

Another free option for hosting Python web apps.

### Setup on PythonAnywhere:

1. **Sign up** at https://www.pythonanywhere.com (free tier available)

2. **Upload your code**
   - Use the Files tab to upload your project
   - Or clone from GitHub

3. **Create a virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 cafeanalyzer
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to Web tab → Add a new web app
   - Choose Flask
   - Point to your `app.py` file
   - Set working directory to your project folder

5. **Reload** and your app is live!

### Features:
- ✅ Full Flask application
- ✅ Easy setup
- ✅ Persistent
- ⚠️ Limited CPU time on free tier

---

## Option 4: Railway - FREE (with limits)

Modern platform with excellent developer experience.

### Setup on Railway:

1. **Sign up** at https://railway.app

2. **Create New Project**
   - Click "Deploy from GitHub repo"
   - Select your repository and branch

3. **Railway auto-detects Python**
   - It will automatically install from `requirements.txt`
   - Set start command to: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Deploy** - Railway handles the rest!

---

## Option 5: Vercel (Static Version)

Similar to GitHub Pages but with more features.

1. **Sign up** at https://vercel.com
2. **Import your Git repository**
3. **Configure**:
   - Framework Preset: Other
   - Root Directory: `docs`
4. **Deploy** - Done!

---

## Option 6: Heroku (Flask App)

Classic platform for hosting web applications.

### Setup on Heroku:

1. **Create `Procfile`** in project root:
   ```
   web: gunicorn app:app
   ```

2. **Add runtime.txt** (optional):
   ```
   python-3.11.0
   ```

3. **Deploy**:
   ```bash
   heroku create cafe-calorie-analyzer
   git push heroku claude/cafe-calorie-dollar-analyzer-SHDCV:main
   ```

⚠️ Note: Heroku no longer has a free tier as of 2022.

---

## Comparison Table

| Platform | Type | Free Tier | Setup Difficulty | Features |
|----------|------|-----------|------------------|----------|
| **GitHub Pages** | Static | ✅ Unlimited | ⭐ Easy | Basic (no scraping) |
| **Render** | Flask | ✅ 750 hrs/mo | ⭐⭐ Medium | Full |
| **PythonAnywhere** | Flask | ✅ Limited | ⭐⭐ Medium | Full |
| **Railway** | Flask | ✅ $5 credit | ⭐ Easy | Full |
| **Vercel** | Static | ✅ Unlimited | ⭐ Easy | Basic (no scraping) |
| **Heroku** | Flask | ❌ Paid only | ⭐⭐ Medium | Full |

---

## Recommendation

- **For simplest setup**: Use **GitHub Pages** with the static version
- **For full features (free)**: Use **Render** or **PythonAnywhere**
- **For best developer experience**: Use **Railway**

The static GitHub Pages version is perfect for most use cases since web scraping often fails due to bot protection anyway. Users can simply upload their menu data as JSON files!
