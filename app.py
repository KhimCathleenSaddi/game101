# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from simulation_engine import calculate_benefits

st.set_page_config(page_title="Nature-Based Solutions Benefits Simulator", page_icon="🌿", layout="wide")

st.title("🌿 Nature-Based Solutions (NbS) Benefits Simulator")
st.write("Adjust how favorable or heavily implemented each Nature-Based Solution is (0 = Strongly Disagree / None, 5 = Strongly Agree / Full Scale). Watch the projected benefits update instantly.")

# Load both CSV files with caching for fast slider updates
@st.cache_data
def load_data():
    nbs_df = pd.read_csv("nbs_data.csv")
    matrix_df = pd.read_csv("benefits_matrix.csv")
    return nbs_df, matrix_df

try:
    df_nbs, df_matrix = load_data()
except FileNotFoundError as e:
    st.error(f"Missing CSV file: {e}. Please ensure both nbs_data.csv and benefits_matrix.csv are in your repository.")
    st.stop()

# Sidebar: Dynamic Sliders generated from nbs_data.csv
st.sidebar.header("🌱 NbS Policy Levers")
st.sidebar.markdown("Set implementation / favorability (0–5):")

user_scores = {}
for _, row in df_nbs.iterrows():
    user_scores[row["id"]] = st.sidebar.slider(
        label=row["nbs_name"],
        min_value=0,
        max_value=5,
        value=int(row["default_score"]),
        help=f"Category: {row['category']}"
    )

# Run simulation calculation using the standalone matrix CSV
benefits_dict = calculate_benefits(user_scores, df_matrix)

# Format data for Plotly bar chart
chart_df = pd.DataFrame({
    "Benefit Category": list(benefits_dict.keys()),
    "Projected Score (0-5 Scale)": list(benefits_dict.values())
})

# Dynamically create metric columns matching the number of benefits in your CSV
cols = st.columns(len(benefits_dict))
for i, (benefit, score) in enumerate(benefits_dict.items()):
    with cols[i]:
        st.metric(label=benefit, value=f"{score} / 5.0")

st.divider()

# Render Bar Graph (0 to 5 scale)
fig = px.bar(
    chart_df,
    x="Benefit Category",
    y="Projected Score (0-5 Scale)",
    text="Projected Score (0-5 Scale)",
    title="Projected Impact of Implemented Nature-Based Solutions",
    color="Benefit Category",
    range_y=[0, 5.0]
)
fig.update_traces(texttemplate="%{text}", textposition="outside")
fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Score (0-5)")

st.plotly_chart(fig, use_container_width=True)