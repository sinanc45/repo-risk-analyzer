from pathlib import Path

import pandas as pd


def create_repository_features():
    input_path = Path("data/processed/repositories.csv")
    output_path = Path("data/processed/repository_features.csv")

    df = pd.read_csv(input_path)

    # Tarih alanlarını datetime'a çevir
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    df["pushed_at"] = pd.to_datetime(df["pushed_at"])

    # Bugünün tarihi
    now = pd.Timestamp.now(tz="UTC")

    # Repo yaşı (gün)
    df["repo_age_days"] = (now - df["created_at"]).dt.days

    # Son güncellemeden beri geçen gün
    df["days_since_update"] = (now - df["updated_at"]).dt.days

    # Son push'tan beri geçen gün
    df["days_since_last_push"] = (now - df["pushed_at"]).dt.days

    # Popülerlik skoru (basit)
    df["popularity_score"] = (
        df["stargazers_count"] * 0.6 +
        df["forks_count"] * 0.3 +
        df["watchers_count"] * 0.1
    )

    # Issue yoğunluğu
    df["issues_to_stars_ratio"] = df["open_issues_count"] / (df["stargazers_count"] + 1)

    # Fork yoğunluğu
    df["forks_to_stars_ratio"] = df["forks_count"] / (df["stargazers_count"] + 1)

    # Repo boyutu kategorisi için basit bilgi
    df["size_per_star"] = df["size"] / (df["stargazers_count"] + 1)

    # Seçeceğimiz son kolonlar
    feature_columns = [
        "full_name",
        "language",
        "stargazers_count",
        "forks_count",
        "open_issues_count",
        "watchers_count",
        "size",
        "repo_age_days",
        "days_since_update",
        "days_since_last_push",
        "popularity_score",
        "issues_to_stars_ratio",
        "forks_to_stars_ratio",
        "size_per_star",
        "visibility",
        "html_url"
    ]

    features_df = df[feature_columns]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    features_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Feature dataset saved to: {output_path}")
    print(features_df.head())