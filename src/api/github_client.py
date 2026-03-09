import os
import requests
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# tokenı al
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def search_repositories(query="language:python", per_page=5):
    """
    GitHub'da repository arar
    """

    url = f"{BASE_URL}/search/repositories"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    return response.json()