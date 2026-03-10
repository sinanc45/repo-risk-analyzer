import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import pandas as pd
import streamlit as st

from src.api.repo_analyzer import analyze_repository
from src.api.repository_search import search_repositories_by_keyword

st.set_page_config(page_title="GitHub Repository Risk Analyzer", layout="wide")

st.title("GitHub Repository Risk Analyzer")
st.write("Analyze live public GitHub repositories with repository metadata and risk scoring.")

# -------------------------------------------------
# SINGLE REPOSITORY ANALYSIS
# -------------------------------------------------

st.subheader("🔎 Analyze a Specific Repository")

repo_name = st.text_input(
    label="Analyze a specific repository",
    placeholder="Enter repository in owner/repo format (e.g., owner/repository)"
)

if st.button("Analyze Repository"):
    with st.spinner("Analyzing repository..."):
        result = analyze_repository(repo_name)

    if result is None:
        st.error("Repository not found")
    else:
        st.success("Repository analyzed successfully")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Stars", result["stars"])
        col2.metric("Forks", result["forks"])
        col3.metric("Open Issues", result["issues"])
        col4.metric("Risk Score", result["risk_score"])
        col5.metric("Risk Level", result["risk_level"])

        st.markdown(f"**Language:** {result['language']}")
        st.markdown(f"**Description:** {result['description'] or 'No description available'}")
        st.markdown(f"[Open Repository]({result['repo_url']})")

# -------------------------------------------------
# KEYWORD SEARCH + LIVE RISK ANALYSIS
# -------------------------------------------------

st.divider()
st.subheader("🌍 Search GitHub Repositories by Keyword")

keyword = st.text_input(
    "Search repositories by keyword",
    placeholder="Type a repository name or keyword to search (e.g., ai, machine learning)"
)

if st.button("Search Repositories"):
    if not keyword.strip():
        st.warning("Please enter a keyword")
    else:
        with st.spinner("Searching repositories..."):
            repositories = search_repositories_by_keyword(keyword)

        if not repositories:
            st.error("No repositories found")
        else:
            analyzed_results = []

            for repo in repositories:
                risk_score = (repo["issues"] + 1) / (repo["stars"] + repo["forks"] + 1)

                if risk_score < 0.1:
                    risk_level = "Low"
                elif risk_score < 0.3:
                    risk_level = "Medium"
                else:
                    risk_level = "High"

                analyzed_results.append({
                    "Repository": repo["full_name"],
                    "Language": repo["language"] or "Unknown",
                    "Stars": repo["stars"],
                    "Forks": repo["forks"],
                    "Open Issues": repo["issues"],
                    "Risk Score": round(risk_score, 4),
                    "Risk Level": risk_level,
                    "Description": repo["description"] or "No description available",
                    "Repository URL": repo["repo_url"]
                })

            results_df = pd.DataFrame(analyzed_results)

            st.success(f"Found {len(results_df)} repositories for '{keyword}'")

            st.subheader("Repository Search Results")
            st.data_editor(
                results_df,
                use_container_width=True,
                hide_index=True,
                disabled=True,
                column_config={
                    "Repository URL": st.column_config.LinkColumn(
                        "Repository URL",
                        display_text="Open Repository"
                    )
                }
            )

            st.subheader("Top 10 Highest Risk Scores from Search Results")
            chart_df = results_df.sort_values(by="Risk Score", ascending=False).head(10)
            st.bar_chart(chart_df.set_index("Repository")["Risk Score"])

