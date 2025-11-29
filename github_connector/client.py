# github_connector/client.py

import os
import time
import logging
from typing import Optional, Dict, Any

import requests
from .custom_exceptions import GitHubAPIError, ResourceNotFound, AuthError

logger = logging.getLogger(__name__)
# A sensible default; the application entrypoint can configure logging further.

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s")


class GitHubClient:
   

    BASE_URL = "https://api.github.com"

    def __init__(self, git_token) -> None:
        """
        Initialize the GitHubClient.

         """
        self._git_token = git_token
        if not self._git_token:
            logger.warning("GITHUB_TOKEN not found in environment.")
        else:
            self.headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {self._git_token}"
            }
            self.authenticated = True

        self.session = requests.Session()

        # Retry policy settings
        self._max_retries = 3
        self._initial_backoff = 1  # seconds

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Internal request method with retry and error handling.
        Retries on HTTP 429 and 403 (rate limiting), using exponential backoff.
        Wraps and raises custom exceptions on failure.
        """
        logger.info("HTTP %s %s", method.upper(), url)

        last_exc: Optional[Exception] = None
        for attempt in range(self._max_retries + 1):
            try:
                response = self.session.request(method, url, headers=self.headers, **kwargs)
            except requests.RequestException as err:
                # Network-level error (DNS, connection reset, etc.)
                last_exc = err
                logger.error("Network error on request to %s: %s", url, err)
                # Wrap it and raise as a GitHubAPIError after exhausting attempts
                if attempt < self._max_retries:
                    backoff = self._initial_backoff * (2 ** attempt)
                    logger.warning("Network error, retrying in %.1f seconds (attempt %d/%d)", backoff, attempt + 1, self._max_retries)
                    time.sleep(backoff)
                    continue
                raise GitHubAPIError(f"Network error while requesting {url}: {err}") from err

            status = response.status_code

            # Retry on rate limiting responses
            if status in (429, 403):
                if attempt < self._max_retries:
                    backoff = self._initial_backoff * (2 ** attempt)
                    logger.warning("Received %d from %s; retrying in %.1f seconds (attempt %d/%d)", status, url, backoff, attempt + 1, self._max_retries)
                    time.sleep(backoff)
                    continue
                # If final attempt fails with 403 and we had no token, give hint
                if status == 403 and not self.authenticated:
                    raise AuthError("Access forbidden (403). Consider setting GITHUB_TOKEN environment variable for authenticated requests.")
                # Exhausted retries
                logger.error("Exhausted retries for %s; last status %d", url, status)
                raise GitHubAPIError(f"Rate limited or access forbidden for {url} (status {status}).")

            # Resource not found
            if status == 404:
                logger.error("Resource not found: %s (status 404)", url)
                raise ResourceNotFound(f"Resource not found: {url}")

            # Other HTTP errors
            if 400 <= status < 600:
                # Try to get useful message from response
                try:
                    msg = response.json()
                except Exception:
                    msg = response.text
                logger.error("HTTP error on %s: status %s response: %s", url, status, msg)
                raise GitHubAPIError(f"HTTP {status} error for {url}: {msg}")

            # Success
            try:
                return response.json()
            except ValueError as err:
                logger.error("Invalid JSON response from %s: %s", url, err)
                raise GitHubAPIError(f"Invalid JSON response from {url}") from err

        # If loop finishes without returning, raise the last exception
        raise GitHubAPIError(f"Failed to request {url}") from last_exc

    def get_repo_details(self, owner: str, repo: str) -> dict:
        """
        Fetch repository details from GitHub.
 
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        data = self._request("GET", url)
        # Return a small subset as example (still full data available)
        return {
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "stargazers_count": data.get("stargazers_count"),
            "forks_count": data.get("forks_count")
        }
    #data

    def get_latest_release(self, owner: str, repo: str) -> dict:
        """
        Fetch the latest release information for a repo.
 
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/releases/latest"
        data = self._request("GET", url)
        # Return key fields
        return {
            "tag_name": data.get("tag_name"),
            "name": data.get("name"),
            "body": data.get("body"),
            "published_at": data.get("published_at"),
            "html_url": data.get("html_url"),
        }
        #data
