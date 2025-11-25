# 🌦️ Weather Vibe Dashboard 3.0

A modern, interactive Streamlit web application for real-time weather tracking and historical trend analysis. Get live weather updates for multiple cities with beautiful visualizations and data persistence.

![Weather Vibe Dashboard](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![OpenWeatherMap API](https://img.shields.io/badge/API-OpenWeatherMap-orange?style=flat-square)

## 🎯 Features

### 🧩 Core Features
- ✅ **Live Weather Data** - Real-time updates from OpenWeatherMap API
- ✅ **Multiple Cities** - Track unlimited favorite cities simultaneously
- ✅ **Persistent Storage** - Auto-saves favorite cities to `favorite_cities.json`
- ✅ **Beautiful Dashboard** - Color-coded weather cards with emoji icons
- ✅ **Real-time Visualizations** - Interactive charts with Plotly
- ✅ **Temperature Comparison** - Bar charts comparing cities
- ✅ **Humidity Tracking** - Humidity comparison across cities
- ✅ **7-Day Trends** - Historical temperature and humidity trends
- ✅ **Data History** - Automatic logging to `weather_history.csv`
- ✅ **Refresh Button** - Manual data updates anytime
- ✅ **Modern UI** - Responsive Streamlit layout with tabs and columns

### 🧠 Advanced Features
- 📊 **Historical Trends** - 7-day temperature and humidity tracking
- 🎨 **Theme Customization** - Modern pastel colors and emoji styling
- 💾 **Data Export** - Download historical data as CSV
- 🔄 **Auto Caching** - Efficient data loading and caching
- 🌍 **Multi-City Support** - Compare weather across the globe
- ⚙️ **Settings Panel** - API key management and temperature unit toggle
- 🔐 **Secure API** - Password-protected API key input
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 📋 Project Structure

```
weather-vibe-dashboard/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── favorite_cities.json        # Stored favorite cities
├── weather_history.csv         # Historical weather data
├── charts/                     # Auto-generated chart directory
│   ├── temperature_trend.png
│   ├── humidity_comparison.png
│   └── ...
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Free API key from [OpenWeatherMap](https://openweathermap.org/api)

### Installation

1. **Clone or Download the Project**
   ```bash
   cd weather-vibe-dashboard
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Your API Key**
   - Visit [https://openweathermap.org/api](https://openweathermap.org/api)
   - Sign up for a free account
   - Copy your API key

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

5. **Open in Browser**
   - The app will automatically open at `http://localhost:8501`
   - Or navigate there manually

## 📖 Usage Guide

### Getting Started
1. **Enter API Key** - Paste your OpenWeatherMap API key in the sidebar
2. **Add Cities** - Type city names and click "Add City"
3. **Select Display** - Choose which cities to view on the dashboard
4. **View Weather** - Watch real-time weather updates and trends

### Features Walkthrough

#### 🌡️ Current Conditions Tab
- Live weather cards for each selected city
- Temperature (in °C or °F)
- Feels-like temperature
- Humidity percentage
- Wind speed
- Atmospheric pressure
- Weather condition with emoji

#### 📈 7-Day Trends Tab
- Historical temperature trends
- Historical humidity trends
- Data table with historical records
- Select different cities to compare

#### ⚙️ Settings Tab
- View app statistics
- Manage data (view, clear, export)
- Download historical data as CSV
- App information and technical stack

### Settings Panel (Sidebar)
- 🔑 **API Key** - Enter/update your OpenWeatherMap API key
- 🌡️ **Temperature Unit** - Toggle between °C and °F
- 🏙️ **Add Cities** - Add new favorite cities
- 🗑️ **Remove Cities** - Delete cities from favorites
- 📍 **Display Cities** - Select which cities to show

## 📊 Data Files

### `favorite_cities.json`
Stores your preferred cities for quick access:
```json
{
  "cities": [
    "Kuala Lumpur",
    "Tokyo",
    "London",
    "New York"
  ]
}
```

### `weather_history.csv`
Historical weather records for trend analysis:
```csv
timestamp,city,temperature_c,humidity,condition
2025-11-12 10:30:45,Kuala Lumpur,29.3,66,Clouds
2025-11-12 10:35:12,Tokyo,21.6,72,Light Rain
2025-11-12 10:40:22,London,16.9,67,Overcast
```

## 🎨 Customization

### Color Scheme
Modify the custom CSS in the app for different themes:
```python
st.markdown("""
<style>
    --primary-color: #FF6B6B;      # Red
    --secondary-color: #4ECDC4;    # Teal
    --success-color: #95E1D3;      # Green
    --warning-color: #FFD93D;      # Yellow
    --danger-color: #FF8E72;       # Orange
</style>
""", unsafe_allow_html=True)
```

### Weather Emojis
Customize emoji mappings for weather conditions:
```python
emoji_map = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'snow': '❄️',
    # Add more mappings...
}
```

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.28+ |
| **API** | OpenWeatherMap |
| **Data Processing** | Pandas |
| **Visualization** | Plotly, Matplotlib |
| **Data Storage** | JSON, CSV |
| **Language** | Python 3.8+ |
| **HTTP Requests** | Requests |

## 📦 Dependencies

```
streamlit==1.28.1
requests==2.32.5
pandas==2.1.3
matplotlib==3.8.2
plotly==5.18.0
python-dateutil==2.8.2
```

## ⚠️ Error Handling

The app gracefully handles:
- ❌ **Invalid API Key** - Shows clear error message
- ❌ **City Not Found** - Alerts user to check spelling
- ❌ **Network Issues** - Connection error notifications
- ❌ **Missing Data** - Friendly fallback messages
- ❌ **Rate Limiting** - Handles API rate limits

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Weather Vibe Dashboard"
   git push origin main
   ```

2. **Create Streamlit Account**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Deploy App**
   - Click "New app"
   - Select your repository and `app.py`
   - Click "Deploy"

4. **Set Secrets** (for API key)
   - Go to app settings
   - Add `OPENWEATHER_API_KEY` in Secrets management

### Deploy Locally
```bash
# Run development server
streamlit run app.py

# Access at: http://localhost:8501
```

## 📈 Optional Enhancements

- [ ] Add weather forecast (5-day, 7-day)
- [ ] Implement local caching with TTL
- [ ] Add dark mode toggle
- [ ] Export charts as PDF
- [ ] Weather alerts and notifications
- [ ] Map view with city markers
- [ ] Weather comparison between dates
- [ ] Air quality index integration
- [ ] UV index tracking
- [ ] ML-based temperature prediction

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - feel free to use it in your projects!

## 🙏 Acknowledgments

- [OpenWeatherMap API](https://openweathermap.org/api) - For weather data
- [Streamlit](https://streamlit.io) - For the amazing framework
- [Plotly](https://plotly.com) - For interactive visualizations

## 📞 Support

- 📧 **Email**: support@weathervibe.app
- 🐛 **Issues**: GitHub Issues
- 💬 **Discussions**: GitHub Discussions

## 🌟 Show Your Support

If you find this project helpful, please:
- ⭐ Star the repository
- 🔄 Share with others
- 💭 Leave feedback
- 🐛 Report issues

---

**Made with ❤️ using Streamlit | Weather Vibe Dashboard 3.0**

*Last Updated: November 12, 2025*
