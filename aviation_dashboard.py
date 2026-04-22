import streamlit as st
import pandas as pd
import os
from deltalake import DeltaTable

st.set_page_config(page_title="Aviation Intelligence", layout="wide")

# Stealth Monochrome Style
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    h1, h2, h3 { color: #ffffff; font-family: 'Helvetica Neue', sans-serif; }
    .stTable { background-color: #111111; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ AVIATION DENSITY ANALYTICS")
st.subheader("Real-time Global Flight Data (Gold Layer)")

# 1. Dynamically find the Data folder (Steps up one level from this file's location)
current_dir = os.path.dirname(os.path.abspath(__file__))
gold_path = os.path.join(current_dir, "data", "gold_aviation_metrics")

try:
    # 2. Read the Delta table instantly using the native Python/Rust library (NO Spark required)
    dt = DeltaTable(gold_path)
    gold_df = dt.to_pandas()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Top Countries by Flight Density")
        st.table(gold_df.head(10))
    
    with col2:
        st.write("### Speed vs Altitude Analysis")
        st.scatter_chart(data=gold_df, x="avg_velocity_ms", y="avg_altitude_m", color="origin_country")

except Exception as e:
    # If it fails, it will now tell you EXACTLY where it tried to look
    st.error(f"Gold Layer not found. Expected it at: {gold_path}")
    st.error(f"System Error: {e}")