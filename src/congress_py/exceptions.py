"""Project-specific exceptions for congress_py."""


class CongressAPIError(Exception):
    """Base exception for congress_py errors."""


class CongressAuthError(CongressAPIError):
    """Base exception for authentication-related errors."""


class MissingAPIKeyError(CongressAuthError):
    """Raised when no Congress.gov API key is available."""


class InvalidAPIKeyError(CongressAuthError):
    """Raised when Congress.gov rejects the provided API key."""
