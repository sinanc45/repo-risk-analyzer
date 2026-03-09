import json
from pathlib import Path

import pandas as pd


def prepare_repositories_dataset():
    input_path = Path("data/raw/repositories.json")
    output_path = Path("data/processed/repositories.csv")

    with open(input_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    repositories = raw_data.get("items", [])

    cleaned_data = []

    for repo in repositories:
        cleaned_data.append({
            "full_name": repo.get("full_name"),
            "name": repo.get("name"),
            "owner": repo.get("owner", {}).get("login"),
            "language": repo.get("language"),
            "stargazers_count": repo.get("stargazers_count"),
            "forks_count": repo.get("forks_count"),
            "open_issues_count": repo.get("open_issues_count"),
            "watchers_count": repo.get("watchers_count"),
            "default_branch": repo.get("default_branch"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "pushed_at": repo.get("pushed_at"),
            "size": repo.get("size"),
            "topics": ", ".join(repo.get("topics", [])),
            "visibility": repo.get("visibility"),
            "html_url": repo.get("html_url")
        })

    df = pd.DataFrame(cleaned_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Processed dataset saved to: {output_path}")
    print(df.head())