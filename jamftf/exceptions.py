"""Custom Exceptions"""

class ImporterConfigError(Exception):
    """error type for incorrect configurations"""

class DataError(Exception):
    """error type for invalid data combinations/tainted data"""

class InvalidResourceTypeError(Exception):
    """raised if invalid resource type key reference."""
