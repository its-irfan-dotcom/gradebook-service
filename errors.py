class GradebookError(Exception):
    """Base exception for gradebook errors."""


class ValidationError(GradebookError):
    """Raised when request data is invalid."""


class NotFoundError(GradebookError):
    """Raised when a requested resource does not exist."""


class ConflictError(GradebookError):
    """Raised when a resource already exists."""