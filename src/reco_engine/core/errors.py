class RecoEngineError(Exception):
    """Base exception for recommendation engine."""


class DataValidationError(RecoEngineError):
    """Raised when required observed data is missing or malformed."""


class ExternalServiceError(RecoEngineError):
    """Raised when Home Assistant API calls fail."""

