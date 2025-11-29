# tests/test_client.py

import json
import requests
from unittest.mock import patch
import pytest
import pytest_mock
import os
from github_connector.client import GitHubClient
from github_connector.custom_exceptions import ResourceNotFound
from dotenv import load_dotenv

load_dotenv()
test_token = os.getenv("GITHUB_TOKEN")


@pytest.fixture
def init_client():
    return GitHubClient(test_token)


def make_response(status=200, payload=None):
    """Helper to build a requests.Response-like object for testing."""
    r = requests.Response()
    r.status_code = status
    r._content = json.dumps(payload or {}).encode("utf-8")
    return r


@patch("github_connector.client.requests.Session.request")
def test_get_repo_details_success(mock_request, init_client):
    # Mock a 200 response
    payload = {
        "full_name": "owner/repo",
        "description": "A repo",
        "stargazers_count": 5,
        "forks_count": 2,
        "html_url": "https://github.com/owner/repo"
    }
    mock_request.return_value = make_response(200, payload)

    client = init_client
    data = client.get_repo_details("owner", "repo")
    assert data["full_name"] == "owner/repo"
    assert data["stargazers_count"] == 5


@patch("github_connector.client.requests.Session.request")
def test_get_repo_details_404_raises(mock_request, init_client):
    mock_request.return_value = make_response(404, {"message": "Not Found"})
    client = init_client
    with pytest.raises(ResourceNotFound):
        client.get_repo_details("owner", "nonexistent")


@patch("github_connector.client.requests.Session.request")
def test_retry_sequence_then_success(mock_request, init_client):
    # Simulate: 429, 429, 200
    payload_ok = {
        "full_name": "owner/repo",
        "description": "A repo",
        "stargazers_count": 10,
        "forks_count": 1,
        "html_url": "https://github.com/owner/repo"
    }
    mock_request.side_effect = [
        make_response(429, {"message": "rate limit"}),
        make_response(429, {"message": "rate limit"}),
        make_response(200, payload_ok),
    ]

    client = init_client
    # Patch time.sleep to avoid real delay during tests
    with patch("time.sleep", return_value=None):
        data = client.get_repo_details("owner", "repo")
    assert data["stargazers_count"] == 10
    # Ensure request was called three times
    assert mock_request.call_count == 3
