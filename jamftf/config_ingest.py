"""manages configuration injest"""

from typing import List
from .constants import ALL_RESOURCE_TYPES, REQUIRED_CONFIG_FLAGS, VALID_CONFIG_KEYS
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





def parse_config_file(config_json: dict) -> List[Resource]:
    """parses a config file"""
    out = []
    for rk in config_json:
        # Validation
        # Valid Resource Types only
        # Valid option keys
        # Required keys not missing

        if rk not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {rk}")

        for i in config_json[rk]:
            if i not in VALID_CONFIG_KEYS:
                raise(DataError(f"invalid config key: {i}"))
        
        for i in REQUIRED_CONFIG_FLAGS:
            if i not in config_json[rk]:
                raise DataError(f"missing required config key: {i}")

        # Skips inactive resources
        if not config_json[rk]["active"]:
            continue

        # Skip these for now but we want the key validated
        if rk == "exclude_ids":
            continue

        opts = Options()
        opts.from_json(config_json[rk])
        print(config_json)

        out.append(
            RESOURCE_TYPE_OBJECT_MAP[rk](options=opts, validate=config_json[rk]["validate"])
        )

    exclude = config_json["exclude_ids"]


    return out
