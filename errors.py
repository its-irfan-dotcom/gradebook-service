
class GradebookError(Exception):
    """Base exception for gradebook errors."""


class ValidationError(GradebookError):
    """Raised when input data is invalid."""


class NotFoundError(GradebookError):
    """Raised when a requested record does not exist."""


class ConflictError(GradebookError):
    """Raised when a record already exists."""
