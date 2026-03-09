from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="GitHub Repository Risk Analyzer", layout="wide")

st.title("GitHub Repository Risk Analyzer")

st.subheader("Analyze a GitHub Repository")

repo_name = st.text_input(
    "Enter repository name (owner/repo)",
    placeholder="facebook/react"
)

if st.button("Analyze Repository"):
    st.info(f"Repository analysis for: {repo_name} coming soon...")

st.write("Analyze repository risk scores generated from GitHub repository metadata.")

data_path = Path("data/processed/repository_risk_scores.csv")

if not data_path.exists():
    st.error("Risk score dataset not found. Run the pipeline first.")
    st.stop()

df = pd.read_csv(data_path)

# ------------------------------
# METRICS
# ------------------------------

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Repositories", len(df))
col2.metric("High Risk Repositories", (df["risk_level"] == "High").sum())
col3.metric("Average Risk Score", round(df["risk_score"].mean(), 3))

# ------------------------------
# SEARCH
# ------------------------------

st.subheader("Search Repository")

search = st.text_input("Search repository name")

if search:
    df = df[df["full_name"].str.contains(search, case=False)]

# ------------------------------
# FILTER
# ------------------------------

st.subheader("Filter Repositories")

risk_levels = st.multiselect(
    "Select risk levels",
    options=sorted(df["risk_level"].unique()),
    default=sorted(df["risk_level"].unique())
)

filtered_df = df[df["risk_level"].isin(risk_levels)]

# ------------------------------
# RISK COLOR FUNCTION
# ------------------------------

def color_risk(val):
    if val == "High":
        return "background-color:#ff4b4b"
    if val == "Medium":
        return "background-color:#ffa500"
    if val == "Low":
        return "background-color:#2ecc71"
    return ""

# ------------------------------
# TABLE
# ------------------------------

st.subheader("Top Risky Repositories")

display_df = filtered_df[
    [
        "full_name",
        "language",
        "stargazers_count",
        "forks_count",
        "open_issues_count",
        "risk_score",
        "risk_level",
        "html_url",
    ]
]

styled_df = display_df.style.applymap(color_risk, subset=["risk_level"])

st.dataframe(styled_df, use_container_width=True)

# ------------------------------
# GRAPH
# ------------------------------

st.subheader("Top 10 Highest Risk Scores")

top10 = filtered_df.sort_values(by="risk_score", ascending=False).head(10)

chart_df = top10.set_index("full_name")["risk_score"]

st.bar_chart(chart_df)