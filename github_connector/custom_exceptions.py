# github_connector/custom_exceptions.py

class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""
    pass


class ResourceNotFound(GitHubAPIError):
    """Raised when a repository or resource is not found (404)."""    
    pass

class AuthError(GitHubAPIError):
    """Raised for authentication-related issues (missing or invalid token)."""
    pass
