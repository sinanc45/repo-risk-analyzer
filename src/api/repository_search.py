import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def search_repositories_by_keyword(keyword, per_page=100):
    url = "https://api.github.com/search/repositories"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    params = {
        "q": f"{keyword} in:name",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    items = data.get("items", [])

    repositories = []

    for repo in items:
        repositories.append({
            "full_name": repo["full_name"],
            "repo_name": repo["name"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "issues": repo["open_issues_count"],
            "language": repo.get("language"),
            "description": repo.get("description"),
            "repo_url": repo["html_url"]
        })

    keyword_lower = keyword.lower()

    repositories.sort(
        key=lambda repo: (
            keyword_lower not in repo["repo_name"].lower(),
            -repo["stars"]
        )
    )

    return repositories