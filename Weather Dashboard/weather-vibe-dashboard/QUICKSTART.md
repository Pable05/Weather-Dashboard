# 🌦️ Weather Vibe Dashboard 3.0 - QUICK START GUIDE

## 🚀 Getting Started in 5 Minutes

### Step 1: Get Your API Key (2 minutes)
1. Visit: https://openweathermap.org/api
2. Click "Sign Up" and create a free account
3. Verify your email
4. Go to "API Keys" section
5. Copy your default API key

### Step 2: Run the App (1 minute)
```bash
cd "c:\Users\USER\Bandawg Projects\Cloocus\Weather Dashboard\weather-vibe-dashboard"
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

### Step 3: Configure & Use (2 minutes)

**In the Sidebar:**
1. 🔑 Paste your API key in "Enter OpenWeatherMap API Key"
2. 🌡️ Choose temperature unit (°C or °F)
3. 🏙️ Add cities you want to track (e.g., "Kuala Lumpur", "Tokyo", "London")
4. 📍 Select which cities to display

**Main Dashboard:**
- 🌡️ **Current Conditions** - Live weather cards for each city
- 📈 **7-Day Trends** - Historical temperature and humidity charts
- ⚙️ **Settings** - Data management and app info

## 🎨 Features Overview

### Real-time Weather Display
```
☀️ Kuala Lumpur — 84.8°F | 66% humidity | Clouds
🌧️ Tokyo — 71°F | 72% humidity | Light Rain
☁️ London — 62°F | 67% humidity | Overcast
```

### Charts & Visualizations
- 🌡️ Temperature comparison bar chart
- 💧 Humidity comparison bar chart
- 📊 7-day temperature trends
- 📉 7-day humidity trends

### Data Persistence
- 📁 `favorite_cities.json` - Your favorite cities (auto-saved)
- 📊 `weather_history.csv` - Historical data for trends

## ⚙️ File Structure

```
weather-vibe-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── favorite_cities.json      # Stored favorite cities
├── weather_history.csv       # Historical weather data
├── charts/                   # Generated charts directory
└── README.md                 # Full documentation
```

## 🎯 Common Tasks

### Add a New City
1. Enter city name in sidebar: "Add a new city"
2. Click "➕ Add City"
3. Select in "📍 Display Cities" to show it

### Remove a City
1. Select city from "Remove a city" dropdown
2. Click "🗑️ Remove City"

### Switch Temperature Units
1. In sidebar, select "🌡️ Temperature Unit"
2. Choose °C or °F (auto-updates dashboard)

### View Historical Data
1. Go to "📈 7-Day Trends" tab
2. Select a city from the dropdown
3. View temperature and humidity trends

### Export Data
1. Go to "⚙️ Settings & Info" tab
2. Click "💾 Export as CSV"
3. Download historical weather data

### Clear History
1. Go to "⚙️ Settings & Info" tab
2. Click "🗑️ Clear History"
3. Confirm to delete all historical records

## 🔑 API Key Tips

**Get Free API Key:**
- Sign up at https://openweathermap.org/api
- Free tier includes current weather API
- Unlimited API calls (with rate limits)
- No credit card required

**Keep Your API Key Safe:**
- Never commit to GitHub without .gitignore
- Use environment variables for production
- Streamlit Cloud supports Secrets management

## 🐛 Troubleshooting

### ❌ "Invalid API Key" Error
- Double-check your API key at openweathermap.org
- Ensure you're using Current Weather API key (not 2.5/weather endpoint)
- Wait a few minutes after account creation

### ❌ "City not found" Error
- Check spelling (case-insensitive)
- Use city names, not abbreviations
- Some small towns may not be available

### ❌ App won't start
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version (3.8+): `python --version`
- Try: `streamlit cache clear` then restart

### ⚠️ Slow charts loading
- Streamlit caches data automatically
- First load may be slower than subsequent loads
- Use "Refresh Weather Data" button to update

## 📈 Tips & Tricks

### Monitor Weather Changes
1. Add cities you care about to favorites
2. Refresh data periodically
3. Check 7-Day Trends to spot patterns
4. Export data for external analysis

### Compare Cities
1. Select multiple cities in sidebar
2. Use comparison charts to analyze
3. Temperature and humidity side-by-side
4. Easily spot regional differences

### Save Chart Screenshots
1. Click camera icon on any chart
2. Automatically saved to `charts/` folder
3. Use for reports or presentations

### Auto-refresh (Advanced)
Streamlit doesn't auto-refresh, but you can:
1. Use browser refresh (F5)
2. Click "🔄 Refresh Weather Data" button
3. Deploy to Streamlit Cloud for scheduled runs

## 🌐 Deployment Options

### Local Development
```bash
streamlit run app.py
```
Runs on `http://localhost:8501`

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Select your repo and app.py
4. Add API key in Secrets management
5. Auto-deploys on push!

### Heroku Deployment
See `README.md` for detailed Heroku setup

## 📚 Resources

- 📖 [Streamlit Docs](https://docs.streamlit.io)
- 🌍 [OpenWeatherMap API](https://openweathermap.org/api)
- 📊 [Plotly Charts](https://plotly.com/python)
- 🐍 [Python Guide](https://python.org)

## 🎓 Learning Path

**Beginner:**
- [ ] Run the app locally
- [ ] Add 3-5 favorite cities
- [ ] View current weather
- [ ] Export data

**Intermediate:**
- [ ] Understand JSON structure
- [ ] Modify favorite_cities.json manually
- [ ] Analyze weather_history.csv in Excel
- [ ] Customize colors in app.py

**Advanced:**
- [ ] Deploy to Streamlit Cloud
- [ ] Add forecast integration
- [ ] Create custom visualizations
- [ ] Build API caching layer

## 🆘 Need Help?

**Check these first:**
1. Review error messages carefully
2. Test API key independently
3. Verify internet connection
4. Check Python version compatibility

**Contact:**
- 📧 Email: support@weathervibe.app
- 🐛 GitHub Issues
- 💬 GitHub Discussions

## ✅ Checklist Before First Run

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] OpenWeatherMap API key obtained
- [ ] Internet connection working
- [ ] Streamlit command recognized in terminal

## 🎉 You're Ready!

```bash
streamlit run app.py
```

**Happy weather tracking! 🌦️**

---

*Last Updated: November 12, 2025*
