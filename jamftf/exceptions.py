"""Custom Exceptions"""

class ImporterConfigError(Exception):
    """Raised when importer configuration is invalid or incompatible."""

class DataError(Exception):
    """Raised when data is corrupt, inconsistent, or fails validation checks."""

class InvalidResourceTypeError(Exception):
    """Raised when an unsupported or non-existent resource type is referenced."""

class OptionsConflictError(Exception):
    """Raised when global and local options have contradictory settings."""
