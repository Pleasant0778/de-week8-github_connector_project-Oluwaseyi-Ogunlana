# GitHub Connector Project

## Overview

The **GitHub Connector Project** is a Python-based tool designed to interact with the GitHub API. It allows you to fetch repository data, releases, commits. The module is designed to meet the needs for a standardized way to fetch repository data from GitHub for a new internal dashboard. Previous attempts using ad-hoc scripts have failed due to rate limiting and poor error handling. Your Task is to build a standalone Python library, github_connector, that abstracts away the complexities of the GitHub API.

## Features

* Connect to GitHub using Personal Access Tokens.
* Fetches general info about a repository (stars, forks, description) and details about the latest release (if available).
* Pytest testing

## Requirements

* Python 3.9+
* Packages in `requirements.txt`:

  ```
  requests
  pandas
  python-dotenv
  pytest
  pytest-mock
  ```

## Run Demo

 
**Create a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   ```

**Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

**Configure environment variables**
   Create a `.env` file in the root directory:

   ```
   GITHUB_TOKEN=your_personal_access_token
   BASE_REPO_URL=https://api.github.com/repos/<owner>/<repo>
   ```

   Replace `<owner>` and `<repo>` with the GitHub repository you want to use for the API call.

**Run the main script**

   ```bash
   poetry run python main.py

(github_con_venv) PS C:\Users\Personal\data_epic\week8\github_connector_project> poetry run python main.py
2025-11-29 21:05:12,190 - INFO : HTTP GET https://api.github.com/repos/Pleasant0778/de-week1-oop-oluwaseyi-ogunlana.
2025-11-29 21:05:13,716 - INFO : Repository: {'full_name': 'Pleasant0778/de-week1-oop-oluwaseyi-ogunlana.', 'description': 'data-epic-week1-OOP-library-project', 'stargazers_count': 0, 'forks_count': 0}
2025-11-29 21:05:13,716 - INFO : HTTP GET https://api.github.com/repos/Pleasant0778/de-week1-oop-oluwaseyi-ogunlana./releases/latest
2025-11-29 21:05:14,101 - ERROR : Resource not found: https://api.github.com/repos/Pleasant0778/de-week1-oop-oluwaseyi-ogunlana./releases/latest (status 404)
2025-11-29 21:05:14,101 - ERROR : No release found or resource not found.
   ```

## Project Structure

```
github_connector_project/
├── github_connector/          # Your package source code
│   ├── __init__.py
│   ├── client.py              # The GitHubClient class
│   └── custom_exceptions.py   # Your custom exception classes
├── tests/                     # Your test suite
│   ├── __init__.py
│   └── test_client.py         # Unit tests using mock
├── main.py                    # A demo script showing how to use your library
├── pyproject.toml             # Poetry configuration and dependencies
├── poetry.lock                # Locked dependencies
├── .gitignore                 # Git ignore file
└── README.md                  # Documentation
```

 
 
