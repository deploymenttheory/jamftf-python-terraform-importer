"""manages configuration injest"""

from typing import List
from .constants import ALL_RESOURCE_TYPES
from .exceptions import InvalidResourceTypeError, DataError
from .resources import (
    Resource,
    Scripts,
    Categories
)
from .options import Options


RESOURCE_TYPE_OBJECT_MAP = {
    "jamfpro_script": Scripts,
    "jamfpro_category": Categories
}



VALID_CONFIG_KEYS = [
    "active", 
    "use_resource_type_as_name",
    "exclude_ids",
    "ignore_illegal_characters"
]

REQUIRED_CONFIG_KEYS = [
    "active"
]

def parse_config_file(config_json: dict) -> List[Resource]:
    """parses a config file"""
    out = []

    for rk in config_json:

        # Invalid resource key
        if rk not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {rk}")

        # Invalid option key // TODO refactor this to extract better logging
        if any(i not in VALID_CONFIG_KEYS for i in config_json[rk]):
            raise DataError("invalid options key found")
        
        # Required keys + refactor as above.
        if any(i not in config_json[rk] for i in REQUIRED_CONFIG_KEYS):
            raise DataError("missing required key")

        # Resource not set to active
        if not config_json[rk]["active"]:
            continue

        opts = Options(_from_json=config_json[rk])
        out.append(
            RESOURCE_TYPE_OBJECT_MAP[rk](options=opts)
        )


    return out
