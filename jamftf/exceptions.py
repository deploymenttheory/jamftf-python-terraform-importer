"""Custom Exceptions"""


class jamftf_importer_config_error(Exception):
    """error type for incorrect configurations"""

class jamftf_data_error(Exception):
    """error type for invalid data combinations/tainted data"""