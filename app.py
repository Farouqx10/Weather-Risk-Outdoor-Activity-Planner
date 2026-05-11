import streamlit as st
from weather import WeatherClient
from analyzer import ActivityRiskAnalyzer
from recommender import RecommendationEngine
from utils import (save_search, load_history, create_entry, save_favourite, load_favourites, clean_location)

st.set_page_config(
    page_title="Weather Risk & Outdoor Activity Planner",
    page_icon="🌤",
    layout="wide"
)
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: #f8fafc;
}

/* Main Headers */
h1, h2, h3 {
    color: #f8fafc;
}

/* Paragraph Text */
p, label {
    color: #cbd5e1 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.5rem;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s ease;
}

/* Button Hover */
.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
    transform: scale(1.03);
    color: white !important;
}

/* Input Boxes */
.stTextInput input {
    background-color: #1e293b;
    color: white;
    border: 2px solid #334155;
    border-radius: 10px;
}

/* Select Boxes */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b;
    border-radius: 10px;
    color: white;
}

/* Metrics Cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #cbd5e1;
    font-size: 16px;
    font-weight: 600;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.05);
    padding: 10px 20px;
    border-radius: 10px;
}
/* Active Tab */
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
}

/* Alerts */
.stSuccess {
    border-radius: 12px;
}

.stWarning {
    border-radius: 12px;
}

.stError {
    border-radius: 12px;
}

.stInfo {
    border-radius: 12px;
}

/* Streamlit top toolbar buttons */
[data-testid="stToolbar"] button {
    background: transparent !important;
    color: white !important;
}

/* Header area */
[data-testid="stHeader"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

weather_client = WeatherClient()
analyzer = ActivityRiskAnalyzer(api_key = "AIzaSyBQ4C4ocPPgbCwqM5TkVDJfqHabEf5vngc")
recommender = RecommendationEngine()

tab1, tab2, tab3 = st.tabs(["🌤 Analyzer", "📜 History", "⭐ Favourites"])

with tab1:

    st.title("🌤 Weather Risk & Outdoor Activity Planner")
    st.caption("AI-powered weather risk analysis for outdoor activities")
    
    st.markdown("---")

    favourites = sorted(load_favourites())

    selected_fav = st.selectbox("Select from your favourites", ["None"] + favourites)

    location_input = st.text_input("Enter your location")
    location = selected_fav if selected_fav != "None" else location_input

    activity = st.selectbox("Select Activity", ["Football", "Jogging", "Picnic", "Travel", "Outdoor Event"])

    if st.button("Analyze"):
        try:
            if not location:
                st.error("Please enter a location")
                st.stop()
            
            location = clean_location(location)

            lat, lon = weather_client.get_coordinates(location)
            
            forecast = weather_client.get_weather(lat,lon)
            risk = analyzer.analyze(activity, forecast)
            tips = recommender.safety_tips(forecast)
            
            st.subheader("🌡 Current Weather")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Temperature:", f"{forecast.temperature} °C")
            with col2:    
                st.metric("Wind:", f"{forecast.windspeed} km/h")
            with col3:
                st.metric("Rain:", forecast.rain)
            
            st.subheader("🚦 Risk Assessment")
            
            if risk == "Safe":
                st.success("Safe")
            elif risk == "Manageable":
                st.warning("Manageable")
            elif risk == "Risky":
                st.error("Risky")
            else:
                st.error("Avoid")

            ai_response = analyzer.ai_analysis(activity, forecast)
            
            st.subheader("AI Insight")
            st.write(ai_response)
            
            best_time = recommender.get_best_time(forecast)
            
            st.subheader("⏰ Best Time")
            st.write(best_time)

            packing = recommender.packing_list(activity)
            
            st.subheader("🎒 Packing List")
            for item in packing:
                st.write("-", item)
            
            st.subheader("⚠ Safety Tips")
            for tip in tips:
                st.info(tip)

            entry = create_entry(location, activity, risk)
            save_search(entry)

        except Exception as e:
            st.error(str(e))

    if location:
       if st.button("⭐ Save location to favourites"):
            save_favourite(location)
            st.success("Saved to favourites!")

with tab2:
    st.subheader("📜 Search History")

    history = load_history()

    if history:
        for item in reversed(history[-10:]):
            st.write(f"{item['time']} | {item['location']} | {item['activity']} | {item['risk']}")
    else:
        st.write("No history yet")

with tab3:
    st.subheader("⭐ Favourite Locations")

    favourites = load_favourites()

    if favourites:
        for fav in favourites:
            st.write("-", fav)
    else:
        st.write("No favourites yet")