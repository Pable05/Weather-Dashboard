import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="🌦️ Weather Vibe Dashboard ",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://openweathermap.org/api",
        "Report a bug": "https://github.com/yourusername/weather-vibe",
        "About": "Weather Vibe Dashboard 3.0 - Your personalized weather companion"
    }
)

# ============================================
# CUSTOM STYLING
# ============================================
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --success-color: #95E1D3;
        --warning-color: #FFD93D;
        --danger-color: #FF8E72;
    }
    
    /* Card styling */
    .weather-card {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZATION & SESSION STATE
# ============================================
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'temp_unit' not in st.session_state:
    st.session_state.temp_unit = "C"
if 'selected_cities' not in st.session_state:
    st.session_state.selected_cities = []

# ============================================
# UTILITY FUNCTIONS
# ============================================

def load_favorite_cities():
    """Load favorite cities from JSON file."""
    if os.path.exists("favorite_cities.json"):
        try:
            with open("favorite_cities.json", "r") as f:
                data = json.load(f)
                return data.get("cities", [])
        except:
            return []
    return []

def save_favorite_cities(cities):
    """Save favorite cities to JSON file."""
    with open("favorite_cities.json", "w") as f:
        json.dump({"cities": list(set(cities))}, f, indent=2)

def load_weather_history():
    """Load weather history from CSV."""
    if os.path.exists("weather_history.csv"):
        try:
            return pd.read_csv("weather_history.csv")
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_weather_data(city, temp_c, humidity, condition):
    """Append weather data to CSV history."""
    history = load_weather_history()
    new_record = pd.DataFrame({
        'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'city': [city],
        'temperature_c': [temp_c],
        'humidity': [humidity],
        'condition': [condition]
    })
    history = pd.concat([history, new_record], ignore_index=True)
    history.to_csv("weather_history.csv", index=False)

def fetch_weather(api_key, city):
    """Fetch weather data from OpenWeatherMap API."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Network error: Unable to connect to OpenWeatherMap API")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            st.error("❌ Invalid API Key")
        elif response.status_code == 404:
            st.error(f"❌ City '{city}' not found")
        else:
            st.error(f"❌ API Error: {response.status_code}")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def get_weather_emoji(condition):
    """Return emoji based on weather condition."""
    condition_lower = condition.lower()
    emoji_map = {
        'clear': '☀️',
        'clouds': '☁️',
        'rain': '🌧️',
        'drizzle': '🌦️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️',
        'smoke': '💨',
        'haze': '🌫️',
        'dust': '🌪️',
        'fog': '🌫️',
        'sand': '🌪️',
        'ash': '💨',
        'squall': '💨',
        'tornado': '🌪️'
    }
    for key, emoji in emoji_map.items():
        if key in condition_lower:
            return emoji
    return '🌤️'

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def get_color_for_condition(condition):
    """Return RGB color based on condition."""
    condition_lower = condition.lower()
    colors = {
        'clear': (255, 193, 7),        # Yellow
        'clouds': (158, 158, 158),     # Gray
        'rain': (33, 150, 243),        # Blue
        'drizzle': (100, 181, 246),    # Light Blue
        'thunderstorm': (63, 81, 181), # Dark Blue
        'snow': (207, 216, 220),       # Light Gray
        'mist': (176, 190, 197),       # Grayish
    }
    for key, color in colors.items():
        if key in condition_lower:
            return color
    return (156, 39, 176)  # Purple default

# ============================================
# SIDEBAR - CONTROLS
# ============================================
st.sidebar.markdown("## ⚙️ Settings & Controls")

# API Key Input
api_key = st.sidebar.text_input(
    "🔑 Enter OpenWeatherMap API Key",
    value=st.session_state.api_key,
    type="password",
    help="Get your free API key from openweathermap.org"
)
st.session_state.api_key = api_key

# Temperature Unit Toggle
st.sidebar.markdown("### 🌡️ Temperature Unit")
temp_unit = st.sidebar.radio("Select unit:", ["°C", "°F"], horizontal=True)
st.session_state.temp_unit = temp_unit[0]

# Load and display favorite cities
favorite_cities = load_favorite_cities()

st.sidebar.markdown("### 🏙️ Manage Cities")

# Add new city
new_city = st.sidebar.text_input(
    "Add a new city",
    placeholder="e.g., New York"
)
if st.sidebar.button("➕ Add City"):
    if new_city and new_city not in favorite_cities:
        favorite_cities.append(new_city)
        save_favorite_cities(favorite_cities)
        st.sidebar.success(f"✅ Added {new_city}")
        st.rerun()

# Select cities to display
st.sidebar.markdown("### 📍 Display Cities")
selected_cities = st.sidebar.multiselect(
    "Choose cities to display:",
    options=favorite_cities,
    default=favorite_cities[:3] if favorite_cities else []
)

# Remove city button
city_to_remove = st.sidebar.selectbox(
    "Remove a city:",
    options=favorite_cities,
    index=None,
    placeholder="Select to remove"
)
if st.sidebar.button("🗑️ Remove City"):
    if city_to_remove in favorite_cities:
        favorite_cities.remove(city_to_remove)
        save_favorite_cities(favorite_cities)
        st.sidebar.success(f"✅ Removed {city_to_remove}")
        st.rerun()

# ============================================
# MAIN HEADER
# ============================================
st.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h1>🌦️ Weather Vibe Dashboard 3.0</h1>
    <p style='font-size: 1.1em; color: #666;'>Live weather updates and trend insights for your favorite cities</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# ERROR HANDLING
# ============================================
if not api_key:
    st.warning("⚠️ Please enter your OpenWeatherMap API key in the sidebar to get started!")
    st.info("Get your free API key at: https://openweathermap.org/api")
elif not selected_cities:
    st.info("📍 Select or add cities in the sidebar to display weather data")
else:
    # ============================================
    # MAIN CONTENT - REFRESH BUTTON
    # ============================================
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button("🔄 Refresh Weather Data", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("💾 Save Charts", use_container_width=True):
            st.session_state.save_charts = True
    
    # ============================================
    # FETCH WEATHER DATA
    # ============================================
    weather_data = {}
    for city in selected_cities:
        data = fetch_weather(api_key, city)
        if data:
            weather_data[city] = data
            # Save to history
            temp_c = data['main']['temp']
            humidity = data['main']['humidity']
            condition = data['weather'][0]['main']
            save_weather_data(city, temp_c, humidity, condition)
    
    if weather_data:
        # ============================================
        # TAB LAYOUT
        # ============================================
        tab1, tab2, tab3 = st.tabs(["🌡️ Current Conditions", "📈 7-Day Trends", "⚙️ Settings & Info"])
        
        # ============================================
        # TAB 1: CURRENT CONDITIONS
        # ============================================
        with tab1:
            st.subheader("Live Weather Cards")
            
            # Create columns for weather cards
            cols = st.columns(min(len(weather_data), 3))
            
            for idx, (city, data) in enumerate(weather_data.items()):
                col = cols[idx % len(cols)]
                
                with col:
                    temp_c = data['main']['temp']
                    temp_f = celsius_to_fahrenheit(temp_c)
                    humidity = data['main']['humidity']
                    condition = data['weather'][0]['main']
                    emoji = get_weather_emoji(condition)
                    feels_like_c = data['main']['feels_like']
                    feels_like_f = celsius_to_fahrenheit(feels_like_c)
                    wind_speed = data['wind']['speed']
                    pressure = data['main']['pressure']
                    
                    # Display temperature based on unit selection
                    if st.session_state.temp_unit == 'F':
                        display_temp = f"{temp_f:.1f}°F"
                        display_feels = f"{feels_like_f:.1f}°F"
                    else:
                        display_temp = f"{temp_c:.1f}°C"
                        display_feels = f"{feels_like_c:.1f}°C"
                    
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                        border-radius: 10px;
                        color: white;
                        text-align: center;
                    '>
                        <h2>{emoji} {city}</h2>
                        <div style='font-size: 2.5em; font-weight: bold; margin: 15px 0;'>{display_temp}</div>
                        <div style='font-size: 1em; opacity: 0.9;'>Feels like {display_feels}</div>
                        <div style='font-size: 1.1em; margin-top: 10px;'>{condition}</div>
                        <hr style='opacity: 0.3; margin: 15px 0;'>
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;'>
                            <div>💧 {humidity}%</div>
                            <div>💨 {wind_speed} m/s</div>
                            <div>🔽 {pressure} hPa</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Temperature comparison chart
            st.markdown("---")
            st.subheader("🌡️ Temperature Comparison")
            
            temp_data = []
            for city, data in weather_data.items():
                temp_c = data['main']['temp']
                temp_f = celsius_to_fahrenheit(temp_c)
                if st.session_state.temp_unit == 'F':
                    temp_data.append({"City": city, "Temperature": temp_f})
                else:
                    temp_data.append({"City": city, "Temperature": temp_c})
            
            df_temp = pd.DataFrame(temp_data)
            
            fig_temp = go.Figure(data=[
                go.Bar(
                    x=df_temp['City'],
                    y=df_temp['Temperature'],
                    marker=dict(
                        color=df_temp['Temperature'],
                        colorscale='RdYlBu_r',
                        showscale=True
                    ),
                    text=[f"{t:.1f}°" for t in df_temp['Temperature']],
                    textposition='auto',
                )
            ])
            fig_temp.update_layout(
                title="Temperature by City",
                xaxis_title="City",
                yaxis_title=f"Temperature ({st.session_state.temp_unit})",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Humidity comparison chart
            st.subheader("💧 Humidity Comparison")
            
            humidity_data = []
            for city, data in weather_data.items():
                humidity_data.append({"City": city, "Humidity": data['main']['humidity']})
            
            df_humidity = pd.DataFrame(humidity_data)
            
            fig_humidity = go.Figure(data=[
                go.Bar(
                    x=df_humidity['City'],
                    y=df_humidity['Humidity'],
                    marker=dict(color='#4ECDC4'),
                    text=[f"{h}%" for h in df_humidity['Humidity']],
                    textposition='auto',
                )
            ])
            fig_humidity.update_layout(
                title="Humidity by City",
                xaxis_title="City",
                yaxis_title="Humidity (%)",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_humidity, use_container_width=True)
        
        # ============================================
        # TAB 2: 7-DAY TRENDS
        # ============================================
        with tab2:
            st.subheader("📈 Historical Weather Trends")
            
            history = load_weather_history()
            
            if not history.empty:
                # Robustly parse both date and datetime formats, strip whitespace, coerce errors
                history['timestamp'] = pd.to_datetime(history['timestamp'].astype(str).str.strip(), errors='coerce')
                
                # Select city for trend
                trend_city = st.selectbox(
                    "Select city to view trend:",
                    options=history['city'].unique()
                )
                
                city_history = history[history['city'] == trend_city].tail(7).copy()
                
                if not city_history.empty:
                    # Temperature trend
                    st.markdown("#### 🌡️ Temperature Trend (Last 7 Days)")
                    
                    fig_trend = go.Figure()
                    
                    fig_trend.add_trace(go.Scatter(
                        x=city_history['timestamp'],
                        y=city_history['temperature_c'],
                        mode='lines+markers',
                        name='Temperature',
                        line=dict(color='#FF6B6B', width=3),
                        marker=dict(size=8)
                    ))
                    
                    fig_trend.update_layout(
                        title=f"Temperature Trend for {trend_city}",
                        xaxis_title="Date",
                        yaxis_title="Temperature (°C)",
                        hovermode='x unified',
                        height=400,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig_trend, use_container_width=True)
                    
                    # Humidity trend
                    st.markdown("#### 💧 Humidity Trend (Last 7 Days)")
                    
                    fig_humidity_trend = go.Figure()
                    
                    fig_humidity_trend.add_trace(go.Scatter(
                        x=city_history['timestamp'],
                        y=city_history['humidity'],
                        mode='lines+markers',
                        name='Humidity',
                        line=dict(color='#4ECDC4', width=3),
                        marker=dict(size=8),
                        fill='tozeroy'
                    ))
                    
                    fig_humidity_trend.update_layout(
                        title=f"Humidity Trend for {trend_city}",
                        xaxis_title="Date",
                        yaxis_title="Humidity (%)",
                        hovermode='x unified',
                        height=400,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig_humidity_trend, use_container_width=True)
                    
                    # Data table
                    st.markdown("#### 📊 Historical Data")
                    st.dataframe(
                        city_history[['timestamp', 'temperature_c', 'humidity', 'condition']].rename(
                            columns={
                                'timestamp': '📅 Time',
                                'temperature_c': '🌡️ Temp (°C)',
                                'humidity': '💧 Humidity (%)',
                                'condition': '☁️ Condition'
                            }
                        ).reset_index(drop=True),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.info("📊 No historical data available yet. Historical data will be collected over time.")
        
        # ============================================
        # TAB 3: SETTINGS & INFO
        # ============================================
        with tab3:
            st.subheader("ℹ️ About This App")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 Features
                
                ✅ **Live Weather Data** - Real-time updates from OpenWeatherMap
                
                ✅ **Multiple Cities** - Track unlimited favorite cities
                
                ✅ **Historical Trends** - 7-day temperature and humidity trends
                
                ✅ **Data Persistence** - Automatic saving to JSON and CSV
                
                ✅ **Beautiful UI** - Responsive design with emojis and colors
                
                ✅ **Temperature Units** - Switch between °C and °F
                
                ✅ **Error Handling** - Graceful error messages and fallbacks
                """)
            
            with col2:
                st.markdown("""
                ### 📚 How to Use
                
                1. **Get API Key** - Sign up at [openweathermap.org](https://openweathermap.org/api)
                
                2. **Add Cities** - Enter city names in the sidebar
                
                3. **Select Display** - Choose which cities to view
                
                4. **Monitor Trends** - Check historical data in the Trends tab
                
                5. **Manage Favorites** - Add/remove cities anytime
                
                ### 🔧 Technical Stack
                
                - **Frontend**: Streamlit
                - **API**: OpenWeatherMap
                - **Data**: Pandas, CSV, JSON
                - **Viz**: Plotly, Matplotlib
                - **Language**: Python 3.8+
                """)
            
            st.markdown("---")
            
            # App statistics
            st.subheader("📊 App Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🏙️ Tracked Cities", len(favorite_cities))
            
            with col2:
                st.metric("👁️ Displayed Cities", len(selected_cities))
            
            with col3:
                history = load_weather_history()
                st.metric("📜 Records Stored", len(history))
            
            with col4:
                st.metric("🌍 Data Points", len(weather_data))
            
            # Data management
            st.markdown("---")
            st.subheader("🗂️ Data Management")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 View Raw Data", use_container_width=True):
                    st.subheader("Raw Weather History")
                    history = load_weather_history()
                    if not history.empty:
                        st.dataframe(history, use_container_width=True)
                    else:
                        st.info("No data available")
            
            with col2:
                if st.button("🗑️ Clear History", use_container_width=True):
                    if os.path.exists("weather_history.csv"):
                        os.remove("weather_history.csv")
                        st.success("✅ History cleared!")
                        st.rerun()
            
            with col3:
                if st.button("💾 Export as CSV", use_container_width=True):
                    history = load_weather_history()
                    if not history.empty:
                        csv = history.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
            
            # Footer
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #999; font-size: 0.9em; margin-top: 20px;'>
                <p>🌦️ Weather Vibe Dashboard 3.0 | Built with ❤️ using Streamlit</p>
                <p>Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p>Made with 💙 | Data from OpenWeatherMap | Deployed on Streamlit</p>
</div>
""", unsafe_allow_html=True)
