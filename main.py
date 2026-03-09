from src.api.github_client import search_repositories


def main():
    repos = search_repositories()

    print("Top Python repositories:\n")

    for repo in repos["items"]:
        name = repo["full_name"]
        stars = repo["stargazers_count"]

        print(f"{name} - ⭐ {stars}")


if __name__ == "__main__":
    main()