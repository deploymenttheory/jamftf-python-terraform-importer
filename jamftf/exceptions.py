"""Custom exceptions for the jamftf package."""

class ConfigError(Exception):
    """Raised when there is an issue with the configuration."""
    pass


class ImporterError(Exception):
    """Raised when there is an issue with the importer."""
    pass


class DataError(Exception):
    """Raised when data is corrupt, inconsistent, or fails validation checks."""


class InvalidResourceTypeError(Exception):
    """Raised when an invalid resource type is provided."""
    pass


class OptionsConflictError(Exception):
    """Raised when global and local options have contradictory settings."""
