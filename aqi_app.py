import streamlit as st
import pandas as pd
import plotly.express as px
import random

# -----------------------------
# Dummy AQI generator
# -----------------------------
def get_random_aqi():
    return random.randint(30, 300)

def get_aqi_status(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Moderate", "yellow"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "orange"
    elif aqi <= 200:
        return "Unhealthy", "red"
    elif aqi <= 300:
        return "Very Unhealthy", "purple"
    else:
        return "Hazardous", "maroon"

# -----------------------------
# Page navigation
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "About"])

# -----------------------------
# Home Page
# -----------------------------
if page == "Home":
    st.title("🌍 Smart AQI Monitoring System")
    st.write("""
    Air pollution is one of the biggest threats to human health today.  
    Our **Smart AQI Monitoring System** uses IoT devices and cloud integration to monitor real-time air quality data.
    
    This prototype shows how AQI can be visualized on a dashboard.
    """)

# -----------------------------
# Dashboard Page
# -----------------------------
elif page == "Dashboard":
    st.title("📊 AQI Dashboard")

    # Define cities and random AQI values
    cities = pd.DataFrame({
        "City": ["Delhi", "Mumbai", "Bangalore", "Kolkata"],
        "lat": [28.61, 19.07, 12.97, 22.57],
        "lon": [77.20, 72.87, 77.59, 88.36],
        "AQI": [get_random_aqi() for _ in range(4)]
    })

    # -----------------------------
    # Plotly Map
    # -----------------------------
    fig_map = px.scatter_mapbox(
        cities,
        lat="lat",
        lon="lon",
        hover_name="City",
        hover_data=["AQI"],
        size="AQI",
        color="AQI",
        color_continuous_scale="RdYlGn_r",
        size_max=30,
        zoom=4,
        height=500
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

    # -----------------------------
    # City selection (simulate click)
    # -----------------------------
    st.subheader("Select a city to see AQI details:")
    city_selected = st.selectbox("City", cities["City"])

    # Generate AQI info for selected city
    current_aqi = get_random_aqi()
    status, color = get_aqi_status(current_aqi)
    st.metric(label=f"Current AQI - {city_selected}", value=current_aqi, delta=status)

    # Line chart for AQI trend
    history = pd.DataFrame({
        "Time": list(range(20)),
        "AQI": [get_random_aqi() for _ in range(20)]
    })
    fig_line = px.line(history, x="Time", y="AQI", title=f"AQI Trend - {city_selected}")
    st.plotly_chart(fig_line)

    # Donut chart for AQI
    fig_donut = px.pie(
        values=[current_aqi, 300 - current_aqi],
        names=["Current AQI", "Remaining to Max"],
        hole=0.6,
        color_discrete_sequence=[color, "lightgrey"]
    )
    fig_donut.update_traces(textinfo="none")
    st.plotly_chart(fig_donut)

# -----------------------------
# About Page
# -----------------------------
elif page == "About":
    st.title("ℹ️ About this Project")
    st.write("""
    This **prototype dashboard** demonstrates how Air Quality Index (AQI) 
    can be monitored and visualized in real-time.

    ### Workflow:
    - **Sensor** → MQ135 + ESP32  
    - **Communication** → 4G SIM / LoRaWAN (MQTT protocol)  
    - **Cloud** → AWS IoT Core + Lambda + DynamoDB  
    - **Visualization** → Web Dashboard

    ⚠️ *Note: This prototype uses random dummy data for demonstration purposes.*
    """)
