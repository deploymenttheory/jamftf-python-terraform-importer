"""manages configuration injest"""

from typing import List
from .constants import ALL_RESOURCE_TYPES
from .exceptions import InvalidResourceTypeError, DataError
from .resources import (
    Resource,
    Scripts,
    Categories,
    Policies
)
from .options import Options


RESOURCE_TYPE_OBJECT_MAP = {
    "jamfpro_script": Scripts,
    "jamfpro_category": Categories,
    "jamfpro_policy": Policies
}

VALID_CONFIG_KEYS = [
    "active", 
    "validate",
    "use_resource_type_as_name",
    "exclude_ids",
    "ignore_illegal_characters"
]

REQUIRED_CONFIG_KEYS = [
    "active",
    "validate"
]

def parse_config_file(config_json: dict) -> List[Resource]:
    """parses a config file"""
    out = []

    for rk in config_json:

        # Invalid resource key
        if rk not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {rk}")

        # Invalid option key
        for i in config_json[rk]:
            if i not in VALID_CONFIG_KEYS:
                raise(DataError(f"invalid config key: {i}"))
        
        # Required option keys
        for i in REQUIRED_CONFIG_KEYS:
            if i not in config_json[rk]:
                raise DataError(f"missing required config key: {i}")

        # Resource not set to active
        if not config_json[rk]["active"]:
            continue

        opts = Options()
        opts.from_json(config_json[rk])

        out.append(
            RESOURCE_TYPE_OBJECT_MAP[rk](options=opts, validate=config_json[rk]["validate"])
        )


    return out
