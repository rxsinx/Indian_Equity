# 🚀 Deployment Guide - Indian Equity Market Analyzer

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [GitHub Repository Setup](#github-repository-setup)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Alternative Deployment Options](#alternative-deployment-options)
5. [Troubleshooting](#troubleshooting)

---

## 1. Local Development Setup

### Prerequisites
- Python 3.8 or higher installed
- Git installed
- Text editor (VS Code, PyCharm, etc.)

### Step-by-Step Installation

#### Step 1: Download/Clone the Project
```bash
# If you have the files locally, navigate to the directory
cd path/to/indian-equity-analyzer

# Or clone from GitHub (after setup)
git clone https://github.com/yourusername/indian-equity-analyzer.git
cd indian-equity-analyzer
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at: `http://localhost:8501`

---

## 2. GitHub Repository Setup

### Initial Setup

#### Step 1: Create GitHub Account
- Go to [github.com](https://github.com)
- Sign up for a free account
- Verify your email

#### Step 2: Create New Repository
1. Click the **"+"** icon in top-right corner
2. Select **"New repository"**
3. Name it: `indian-equity-analyzer`
4. Description: "Master Trader Grade Technical Analysis for Indian Equity Markets"
5. Choose **Public** (for free Streamlit Cloud deployment)
6. **DON'T** initialize with README (we already have one)
7. Click **"Create repository"**

#### Step 3: Push Code to GitHub

```bash
# Navigate to your project directory
cd path/to/indian-equity-analyzer

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Indian Equity Market Analyzer"

# Add remote repository (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/indian-equity-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Updating Repository Later

```bash
# After making changes
git add .
git commit -m "Description of changes"
git push
```

---

## 3. Streamlit Cloud Deployment

### Why Streamlit Cloud?
- ✅ **FREE** hosting for public apps
- ✅ Automatic updates from GitHub
- ✅ Easy deployment process
- ✅ No server management needed

### Deployment Steps

#### Step 1: Create Streamlit Account
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. Authorize Streamlit to access your repositories

#### Step 2: Deploy Your App
1. Click **"New app"** button
2. Select your repository: `indian-equity-analyzer`
3. Branch: `main`
4. Main file path: `app.py`
5. Click **"Deploy!"**

#### Step 3: Wait for Deployment
- First deployment takes 2-5 minutes
- Streamlit Cloud will:
  - Clone your repository
  - Install dependencies from `requirements.txt`
  - Start your application
  - Generate a public URL

#### Step 4: Access Your App
- Your app will be available at: `https://yourusername-indian-equity-analyzer.streamlit.app`
- Share this URL with anyone!

### Automatic Updates
- Every time you push to GitHub, Streamlit Cloud **automatically redeploys**
- No manual intervention needed

---

## 4. Alternative Deployment Options

### Option A: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

### Option B: AWS EC2

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

### Option C: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t equity-analyzer .
docker run -p 8501:8501 equity-analyzer
```

### Option D: Local Network Sharing

```bash
# Find your local IP
# Windows: ipconfig
# Mac/Linux: ifconfig

# Run Streamlit with network access
streamlit run app.py --server.address=0.0.0.0

# Others on same network can access via:
# http://your-local-ip:8501
```

---

## 5. Troubleshooting

### Common Issues

#### Issue 1: "Module not found" Error
**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

#### Issue 2: yfinance Not Fetching Data
**Possible Causes:**
- Wrong stock symbol (should be without .NS suffix)
- Internet connection issues
- Yahoo Finance API temporarily down

**Solution:**
Try adding `.NS` or `.BO` manually:
```python
# In app.py, modify:
ticker_symbol = f"{self.symbol}.NS"  # For NSE
# or
ticker_symbol = f"{self.symbol}.BO"  # For BSE
```

#### Issue 3: Streamlit Cloud Deployment Fails
**Check:**
1. Repository is public
2. `requirements.txt` exists and is correct
3. No syntax errors in `app.py`
4. Check build logs in Streamlit Cloud dashboard

#### Issue 4: Charts Not Displaying
**Solution:**
```bash
pip install --upgrade plotly
```

#### Issue 5: Data Fetching is Slow
**Optimization:**
- Reduce analysis period
- Use caching:
```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_data(symbol, period):
    # ... fetch logic
```

### Getting Help

#### Option 1: Check Logs
```bash
# Local deployment
streamlit run app.py --logger.level=debug

# Streamlit Cloud
# Check logs in Streamlit Cloud dashboard
```

#### Option 2: Community Support
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/yourusername/indian-equity-analyzer/issues)
- Stack Overflow with tags: `streamlit`, `python`, `yfinance`

---

## 6. Performance Optimization

### Caching Data
Add caching to reduce API calls:

```python
@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_stock_data(symbol, period):
    analyzer = IndianEquityAnalyzer(symbol, period)
    analyzer.fetch_data()
    return analyzer
```

### Optimize Chart Rendering
```python
# Limit data points for faster rendering
df = analyzer.data.tail(200)  # Instead of full history
```

### Reduce Memory Usage
```python
# Use smaller data types
df['Close'] = df['Close'].astype('float32')
```

---

## 7. Maintenance Checklist

### Weekly
- [ ] Check if app is running
- [ ] Monitor error logs
- [ ] Test with sample stocks

### Monthly
- [ ] Update dependencies
- [ ] Review and update pattern detection logic
- [ ] Check yfinance library compatibility

### Quarterly
- [ ] Add new features based on user feedback
- [ ] Optimize performance
- [ ] Update documentation

---

## 8. Security Best Practices

### Environment Variables
If adding API keys in the future:

```python
# .streamlit/secrets.toml
api_key = "your-secret-key"

# In app.py
import streamlit as st
api_key = st.secrets["api_key"]
```

### Don't Commit Sensitive Data
- Add `.env` files to `.gitignore`
- Never commit API keys
- Use Streamlit secrets for production

---

## 9. Advanced Configuration

### Custom Streamlit Config
Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

---

## 10. Monitoring & Analytics

### Add Google Analytics (Optional)
In `app.py`:
```python
# Add to HTML head
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
""", unsafe_allow_html=True)
```

### Track Usage
Use Streamlit's built-in analytics:
- Visit Streamlit Cloud dashboard
- Check "Analytics" tab
- Monitor:
  - Daily active users
  - Session duration
  - Error rates

---

## Quick Reference Commands

```bash
# Local Development
streamlit run app.py                    # Run app
streamlit run app.py --server.port 8080 # Custom port
streamlit run app.py --logger.level=debug # Debug mode

# Git Commands
git status                              # Check changes
git add .                              # Stage all changes
git commit -m "message"                # Commit changes
git push                               # Push to GitHub

# Virtual Environment
source venv/bin/activate               # Activate (Mac/Linux)
venv\Scripts\activate                  # Activate (Windows)
deactivate                             # Deactivate

# Package Management
pip list                               # List installed packages
pip freeze > requirements.txt          # Update requirements
pip install -r requirements.txt        # Install from requirements
```

---

**Happy Deploying! 🚀**

For questions or support, open an issue on GitHub or contact the maintainer.
