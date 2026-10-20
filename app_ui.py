# app_ui.py
import os
import streamlit as st
import requests

# Page configuration & layout styling
st.set_page_config(
    page_title="AgriIntelligence Dashboard",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the earthy, warm design theme (Terracotta & Sand)
st.markdown("""
    <style>
    /* Main background and font styling */
    .main {
        background-color: #F9F6F0;
        color: #2C2C2C;
    }
    .stApp {
        background-color: #F9F6F0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2C2C2C;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Custom buttons with Ochre/Terracotta accent */
    .stButton>button {
        background-color: #C86D51;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #B55B3F;
        color: white;
    }
    
    /* Metric Card styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #C86D51;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Determine API URL (supports Docker Compose service name or local fallback)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# App Header
st.title("🌾 Agricultural Yield Intelligence")
st.markdown("### Field Telemetry & Crop Performance Predictor")
st.write("Adjust the environmental telemetry parameters below to estimate expected crop yield using your containerized machine learning backend.")

# Sidebar metadata / settings
with st.sidebar:
    st.markdown("### System Status")
    st.info(f"Backend Target: `{API_URL}`")
    st.markdown("---")
    st.markdown("**Design Theme:** Earthy Road Journey (Terracotta & Sand)")

# Main Input Section inside an aesthetic form layout
with st.container():
    st.markdown("#### 📊 Enter Field Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        soil_moisture_pct = st.slider(
            "Soil Moisture (%)", 
            min_value=10.0, 
            max_value=50.0, 
            value=30.0, 
            step=0.5,
            help="Percentage of moisture content in the soil matrix."
        )
        temperature_c = st.slider(
            "Ambient Temperature (°C)", 
            min_value=10.0, 
            max_value=45.0, 
            value=24.0, 
            step=0.5,
            help="Average ambient temperature during the growth cycle."
        )

    with col2:
        ph_level = st.slider(
            "Soil pH Level", 
            min_value=4.0, 
            max_value=9.0, 
            value=6.5, 
            step=0.1,
            help="Acidity or alkalinity measure of the soil."
        )
        rainfall_mm = st.slider(
            "Seasonal Rainfall (mm)", 
            min_value=20.0, 
            max_value=300.0, 
            value=120.0, 
            step=5.0,
            help="Total cumulative rainfall recorded in millimeters."
        )

st.markdown("<br>", unsafe_allow_html=True)

# Prediction Execution Block
if st.button("Calculate Yield Prediction", use_container_width=True):
    
    # Payload matching FastAPI Pydantic schema and model feature expectations
    payload = {
        "soil_moisture_pct": soil_moisture_pct,
        "temperature_c": temperature_c,
        "ph_level": ph_level,
        "rainfall_mm": rainfall_mm
    }
    
    with st.spinner("Analyzing telemetry data across models..."):
        try:
            # Send request to FastAPI backend
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                prediction_value = result.get("prediction", [0])[0]
                
                st.markdown("---")
                st.success("✨ Prediction Generated Successfully!")
                
                # Display aesthetic metric card
                col_res1, col_res2 = st.columns([2, 1])
                with col_res1:
                    st.metric(
                        label="Estimated Crop Yield", 
                        value=f"{prediction_value:.2f} t/ha", 
                        delta="Optimal Range" if 15 <= prediction_value <= 25 else "Review Conditions"
                    )
                with col_res2:
                    st.write("")
                    st.markdown("**Confidence:** High")
                    st.markdown("**Engine:** Random Forest")
            else:
                st.error(f"Server responded with error code {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error(f"⚠️ **Connection Error:** Could not reach the FastAPI backend at `{API_URL}`. Ensure your Docker container or server is running!")
        except requests.exceptions.Timeout:
            st.error("⚠️ **Timeout:** The backend server took too long to respond.")