from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Repository Risk Dashboard", layout="wide")

st.title("GitHub Repository Risk Analyzer")
st.write("Analyze repository risk scores generated from GitHub repository metadata.")

data_path = Path("data/processed/repository_risk_scores.csv")

if not data_path.exists():
    st.error("Risk score dataset not found. Please run the pipeline first.")
    st.stop()

df = pd.read_csv(data_path)

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Repositories", len(df))
col2.metric("High Risk Repositories", (df["risk_level"] == "High").sum())
col3.metric("Average Risk Score", round(df["risk_score"].mean(), 3))

st.subheader("Filter Repositories")

risk_levels = st.multiselect(
    "Select risk levels",
    options=sorted(df["risk_level"].unique()),
    default=sorted(df["risk_level"].unique())
)

filtered_df = df[df["risk_level"].isin(risk_levels)]

st.subheader("Top Risky Repositories")
st.dataframe(
    filtered_df.sort_values(by="risk_score", ascending=False),
    use_container_width=True
)

st.subheader("Top 10 Highest Risk Scores")
top_10 = filtered_df.sort_values(by="risk_score", ascending=False).head(10)
st.bar_chart(top_10.set_index("full_name")["risk_score"])