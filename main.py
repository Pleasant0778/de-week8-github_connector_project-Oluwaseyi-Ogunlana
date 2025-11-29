# main.py

"""
Demo usage of GitHubClient.

Requires:
    pip install -r requirements (or via poetry)
Set GITHUB_TOKEN in your environment or in a .env file.
"""

from dotenv import load_dotenv
import os
import logging

from github_connector.client import GitHubClient
from github_connector.custom_exceptions import GitHubAPIError, ResourceNotFound, AuthError

 
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s")

def main():

    git_token = os.getenv("GITHUB_TOKEN")

    client = GitHubClient(git_token)

    owner = "Pleasant0778"
    repo = "de-week1-oop-oluwaseyi-ogunlana."

    try:
        repo_info = client.get_repo_details(owner, repo)
        logging.info("Repository: %s", repo_info)
    except ResourceNotFound:
        logging.error("Repository not found.")
    except AuthError as e:
        logging.error("Authentication issue: %s", e)
    except GitHubAPIError as e:
        logging.error("GitHub API error: %s", e)

    try:
        release = client.get_latest_release(owner, repo)
        logging.info("Latest release: %s", release)
    except ResourceNotFound:
        logging.error("No release found or resource not found.")
    except GitHubAPIError as e:
        logging.error("GitHub API error: %s", e)


if __name__ == "__main__":
    main()
