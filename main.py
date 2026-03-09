from src.api.repo_fetcher import fetch_and_save_repositories


def main():
    fetch_and_save_repositories(per_page=10)


if __name__ == "__main__":
    main()