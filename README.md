# GitHub Connector Project

## Overview

The **GitHub Connector Project** is a Python-based library designed to interact with the GitHub API. It allows you to fetch repository metadata, commits, and release information in a standardized way. The library abstracts away the complexities of the GitHub API, providing a clean interface for internal dashboards and data analysis.

## Features

* Connect to GitHub using Personal Access Tokens.
* Fetch repository details (stars, forks, description) and latest release info.
* Pytest-based testing framework included.

## Requirements

* Python 3.9+
* Dependencies (managed via Poetry or `requirements.txt`):

  ```text
  requests
  pandas
  python-dotenv
  pytest      # dev dependency
  pytest-mock # dev dependency
  ```

## Setup and Run

### Using Poetry (recommended)

```bash
# Install dependencies
poetry install

# Activate Poetry shell (optional)
poetry shell

# Run demo script
poetry run python main.py
```

### Environment Configuration

Create a `.env` file in the project root:
make ah buy com
```text
GITHUB_TOKEN=personal_access_token_from_github
BASE_REPO_URL=https://api.github.com/repos/<owner>/<repo>
```

Replace `<owner>` and `<repo>` with your target GitHub repository **without a trailing dot**.

### Expected Output Examplerea

```text
2025-11-29 21:05:12,190 - INFO : HTTP GET https://api.github.com/repos/Pleasant0778/de-week1-oop-oluwaseyi-ogunlana
2025-11-29 21:05:13,716 - INFO : Repository: {'full_name': 'Pleasant0778/de-week1-oop-oluwaseyi-ogunlana', 'description': 'data-epic-week1-OOP-library-project', 'stargazers_count': 0, 'forks_count': 0}
2025-11-29 21:05:13,716 - INFO : HTTP GET https://api.github.com/repos/Pleasant0778/de-week1-oop-oluwaseyi-ogunlana/releases/latest
2025-11-29 21:05:14,101 - ERROR : Resource not found: https://api.github.com/repos/Pleasant0778/de-week1-oop-oluwaseyi-ogunlana/releases/latest (status 404)
2025-11-29 21:05:14,101 - ERROR : No release found or resource not found.
```

## Project Structure

```
github_connector_project/
├── github_connector/          # Package source code
│   ├── __init__.py
│   ├── client.py              # GitHubClient class
│   └── custom_exceptions.py   # Custom exceptions
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test_client.py
├── main.py                    # Demo script
├── pyproject.toml             # Poetry configuration
├── poetry.lock                # Locked dependencies
├── .gitignore                 # Files to ignore in git
└── README.md                  # Project documentation
```
 