# 🔧 Configuration & Customization Guide

## Advanced Setup & Customization

### Environment Variables (.env)
Create a `.env` file to manage secrets:

```bash
# .env file
OPENWEATHER_API_KEY=your_api_key_here
APP_THEME=light
DEBUG_MODE=false
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')
```

### Streamlit Configuration (.streamlit/config.toml)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"

[server]
port = 8501
headless = true
```

### Customize Colors

Edit the color scheme in `app.py`:

```python
st.markdown("""
<style>
    :root {
        --primary-color: #FF6B6B;      # Change these
        --secondary-color: #4ECDC4;
        --success-color: #95E1D3;
        --warning-color: #FFD93D;
        --danger-color: #FF8E72;
    }
</style>
""", unsafe_allow_html=True)
```

### Add Custom Weather Icons

Modify emoji mapping:

```python
emoji_map = {
    'clear': '☀️',
    'sunny': '🌞',
    'clouds': '☁️',
    'cloudy': '🌥️',
    'rain': '🌧️',
    'rainy': '⛈️',
    'drizzle': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'snowy': '🌨️',
    'mist': '🌫️',
    'foggy': '🌁️',
    'wind': '💨',
    'windy': '🌪️',
}
```

### Custom Color Gradients

Add background gradients to cards:

```python
gradient_colors = {
    'clear': 'linear-gradient(135deg, #FFD93D 0%, #FFA500 100%)',
    'clouds': 'linear-gradient(135deg, #B0C4DE 0%, #778899 100%)',
    'rain': 'linear-gradient(135deg, #4682B4 0%, #1E90FF 100%)',
    'snow': 'linear-gradient(135deg, #F0F8FF 0%, #B0E0E6 100%)',
    'thunderstorm': 'linear-gradient(135deg, #36393F 0%, #2C2F33 100%)',
}
```

### Performance Optimization

#### Enable Caching
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_weather_cached(api_key, city):
    return fetch_weather(api_key, city)

@st.cache_resource
def init_connection():
    return requests.Session()
```

#### Limit API Calls
```python
import time

# Rate limiting
if 'last_api_call' not in st.session_state:
    st.session_state.last_api_call = 0

time_since_last = time.time() - st.session_state.last_api_call
if time_since_last < 60:  # Minimum 60 seconds between calls
    st.warning(f"⏳ Please wait {60 - int(time_since_last)}s before refreshing")
else:
    st.session_state.last_api_call = time.time()
```

### Data Analysis Features

#### Add Forecast
```python
def fetch_forecast(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    return requests.get(url).json()
```

#### Temperature Prediction
```python
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_temperature(history_df):
    X = np.arange(len(history_df)).reshape(-1, 1)
    y = history_df['temperature_c'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    next_day = np.array([[len(history_df)]])
    prediction = model.predict(next_day)[0]
    
    return prediction
```

#### Weather Alerts
```python
def check_alerts(city_data):
    alerts = []
    
    if city_data['main']['temp'] > 35:
        alerts.append("🔥 High temperature warning!")
    
    if city_data['main']['humidity'] > 90:
        alerts.append("💧 Very humid - stay hydrated!")
    
    if city_data['wind']['speed'] > 10:
        alerts.append("💨 Strong wind warning!")
    
    if 'rain' in city_data['weather'][0]['main'].lower():
        alerts.append("🌧️ Rainy weather - bring umbrella!")
    
    return alerts
```

### Database Integration

#### SQLite for Persistent Storage
```python
import sqlite3

def init_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_logs
                 (id INTEGER PRIMARY KEY, timestamp TEXT, 
                  city TEXT, temp REAL, humidity INTEGER)''')
    conn.commit()
    return conn

def save_to_db(conn, city, temp, humidity):
    c = conn.cursor()
    c.execute("INSERT INTO weather_logs VALUES (?, ?, ?, ?, ?)",
              (None, datetime.now(), city, temp, humidity))
    conn.commit()
```

#### PostgreSQL for Production
```python
import psycopg2

def connect_postgres(db_url):
    conn = psycopg2.connect(db_url)
    return conn

def save_weather_pg(conn, city, temp, humidity):
    cur = conn.cursor()
    cur.execute("INSERT INTO weather (city, temperature, humidity) VALUES (%s, %s, %s)",
                (city, temp, humidity))
    conn.commit()
```

### Mobile Responsiveness

Add to Streamlit config:
```toml
[client]
toolbarMode = "minimal"
showSidebarNavigation = true

[ui]
hideTopOfPageDecoration = false
hideMainMenuButton = false
```

### Dark Mode Support
```python
import streamlit as st

theme = st.selectbox("🌓 Theme:", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
        body { background-color: #1e1e1e; color: #ffffff; }
        .main { background-color: #1e1e1e; }
    </style>
    """, unsafe_allow_html=True)
```

### Multi-language Support
```python
language = st.selectbox("🌐 Language:", ["English", "Español", "中文", "日本語"])

translations = {
    "English": {"refresh": "Refresh", "add": "Add City"},
    "Español": {"refresh": "Actualizar", "add": "Añadir Ciudad"},
    "中文": {"refresh": "刷新", "add": "添加城市"},
    "日本語": {"refresh": "更新", "add": "都市を追加"},
}

t = translations[language]
```

### File Upload Feature
```python
st.sidebar.markdown("### 📁 Import Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)
```

### Real-time Notifications
```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(recipient, subject, body):
    smtp_server = "smtp.gmail.com"
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
```

### Advanced Analytics
```python
import plotly.express as px

# Heatmap of temperatures
def temperature_heatmap(history_df):
    pivot = history_df.pivot_table(
        index='city',
        columns='timestamp',
        values='temperature_c'
    )
    
    fig = px.imshow(pivot, title="Temperature Heatmap")
    st.plotly_chart(fig, use_container_width=True)

# Weather distribution pie chart
def weather_distribution(history_df):
    dist = history_df['condition'].value_counts()
    fig = px.pie(values=dist.values, names=dist.index, title="Weather Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Time series with moving average
def moving_average(history_df, window=7):
    history_df['MA'] = history_df['temperature_c'].rolling(window=window).mean()
    fig = px.line(history_df, x='timestamp', y=['temperature_c', 'MA'])
    st.plotly_chart(fig, use_container_width=True)
```

### API Rate Limiting

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls, time_window_seconds):
        self.max_calls = max_calls
        self.time_window = timedelta(seconds=time_window_seconds)
        self.calls = []
    
    def is_allowed(self):
        now = datetime.now()
        self.calls = [call for call in self.calls if call > now - self.time_window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

limiter = RateLimiter(max_calls=60, time_window_seconds=60)

if not limiter.is_allowed():
    st.error("⏳ Rate limit exceeded. Please wait before making another request.")
```

### Version Control Best Practices

Create `.gitignore`:
```
# Secrets
*.env
secrets.toml
.streamlit/secrets.toml

# Data files
*.csv
weather.db

# Cache
__pycache__/
*.pyc
.streamlit/cache

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# API Keys (NEVER commit!)
*.key
*.pem
```

### Docker Containerization

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  weather-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
    volumes:
      - ./data:/app/data
```

Run with:
```bash
docker-compose up
```

---

**Pro Tips:**
- Use `@st.cache_data` for expensive computations
- Minimize API calls with smart caching
- Store sensitive data in `.streamlit/secrets.toml`
- Use environment variables in production
- Monitor performance with Streamlit's profiler
- Test extensively before deployment

---

*Last Updated: November 12, 2025*
