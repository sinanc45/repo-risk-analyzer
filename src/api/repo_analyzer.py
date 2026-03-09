import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def analyze_repository(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    stars = data["stargazers_count"]
    forks = data["forks_count"]
    issues = data["open_issues_count"]

    risk_score = (issues + 1) / (stars + forks + 1)

    if risk_score < 0.1:
        risk_level = "Low"
    elif risk_score < 0.3:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "name": repo_name,
        "stars": stars,
        "forks": forks,
        "issues": issues,
        "risk_score": round(risk_score, 4),
        "risk_level": risk_level
    }

