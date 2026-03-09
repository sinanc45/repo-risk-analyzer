from pathlib import Path

import pandas as pd


def min_max_normalize(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([0.0] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val)


def calculate_repository_risk_scores():
    input_path = Path("data/processed/repository_features.csv")
    output_path = Path("data/processed/repository_risk_scores.csv")

    df = pd.read_csv(input_path)

    # Risk artıran faktörler
    df["norm_open_issues"] = min_max_normalize(df["open_issues_count"])
    df["norm_days_since_update"] = min_max_normalize(df["days_since_update"])
    df["norm_days_since_last_push"] = min_max_normalize(df["days_since_last_push"])
    df["norm_issues_to_stars_ratio"] = min_max_normalize(df["issues_to_stars_ratio"])
    df["norm_size_per_star"] = min_max_normalize(df["size_per_star"])

    # Risk azaltan faktörler
    df["norm_stars"] = min_max_normalize(df["stargazers_count"])
    df["norm_forks"] = min_max_normalize(df["forks_count"])
    df["norm_popularity"] = min_max_normalize(df["popularity_score"])

    # Basit risk skoru formülü
    df["risk_score"] = (
        df["norm_open_issues"] * 0.20 +
        df["norm_days_since_update"] * 0.20 +
        df["norm_days_since_last_push"] * 0.20 +
        df["norm_issues_to_stars_ratio"] * 0.20 +
        df["norm_size_per_star"] * 0.10 +
        (1 - df["norm_stars"]) * 0.05 +
        (1 - df["norm_forks"]) * 0.025 +
        (1 - df["norm_popularity"]) * 0.025
    )

    df["risk_score"] = df["risk_score"].round(4)

    # Risk seviyesi etiketi
    def label_risk(score: float) -> str:
        if score >= 0.70:
            return "High"
        if score >= 0.40:
            return "Medium"
        return "Low"

    df["risk_level"] = df["risk_score"].apply(label_risk)

    result_columns = [
        "full_name",
        "language",
        "stargazers_count",
        "forks_count",
        "open_issues_count",
        "days_since_update",
        "days_since_last_push",
        "issues_to_stars_ratio",
        "size_per_star",
        "popularity_score",
        "risk_score",
        "risk_level",
        "html_url"
    ]

    result_df = df[result_columns].sort_values(by="risk_score", ascending=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Risk score dataset saved to: {output_path}")
    print(result_df.head())