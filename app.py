# app.py
import streamlit as st
import plotly.express as px
from simulation_engine import run_simulation

st.set_page_config(page_title="Climate Policy Simulator", page_icon="🌍", layout="wide")

st.title("🌍 Climate Policy Game: Prototype")
st.write("Adjust the policy levers below to see real-time impacts on global temperature and carbon emissions.")

# Sidebar or main inputs for sliders
st.sidebar.header("Policy Controls")
carbon_tax = st.sidebar.slider("Carbon Price ($/ton)", 0, 150, 20)
clean_subsidy = st.sidebar.slider("Clean Energy Subsidies (0-100)", 0, 100, 30)

# Run simulation math from your separate engine file
temp, emissions = run_simulation(carbon_tax, clean_subsidy)

# Display core metrics
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Projected Temperature in 2100", 
        value=f"{temp} °C", 
        delta=f"{round(temp - 3.5, 2)} °C vs Baseline"
    )
with col2:
    st.metric(
        label="Global CO2 Emissions", 
        value=f"{emissions} Gt", 
        delta=f"{round(emissions - 40.0, 1)} Gt vs Baseline"
    )

st.divider()

# Interactive Chart
chart_data = {
    "Year": [2020, 2040, 2060, 2080, 2100],
    "Emissions (Gt)": [35.0, emissions * 0.95, emissions * 0.85, emissions * 0.7, emissions]
}
fig = px.line(chart_data, x="Year", y="Emissions (Gt)", title="Simulated CO2 Emissions Pathway to 2100", markers=True)
st.plotly_chart(fig, use_container_width=True)
