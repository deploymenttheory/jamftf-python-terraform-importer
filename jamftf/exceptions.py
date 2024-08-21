"""Custom Exceptions"""


class importer_config_error(Exception):
    """error type for incorrect configurations"""

class data_error(Exception):
    """error type for invalid data combinations/tainted data"""