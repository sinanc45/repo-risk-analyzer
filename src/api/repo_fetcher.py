import json
from pathlib import Path

from src.api.github_client import search_repositories


def fetch_and_save_repositories(query="language:python", per_page=10):
    data = search_repositories(query=query, per_page=per_page)

    output_path = Path("data/raw/repositories.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Repository data saved to: {output_path}")