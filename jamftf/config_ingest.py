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
    exclude_block = {}

    if "exclude_ids" in config_json:
        exclude_block = config_json["exclude_ids"]

        for rk in exclude_block:
            if rk not in ALL_RESOURCE_TYPES:
                raise DataError("invalid resource key in exclude block")
            
    if "resources" not in config_json:
        raise KeyError("resources block not present in config file")


    resources = config_json["resources"]
    for rk in resources:

        if rk not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {rk}")

        for i in resources[rk]:
            if i not in VALID_CONFIG_KEYS:
                raise DataError(f"invalid config key: {i}")
        
        for i in REQUIRED_CONFIG_FLAGS:
            if i not in resources[rk]:
                raise DataError(f"missing required config key: {i}")

        if not resources[rk]["active"]:
            continue

        opts = Options().from_json(resources)
        validate = resources[rk]["validate"]
        assert isinstance(validate, bool), "validate key is not a bool"

        exclude_ids = []
        if rk in exclude_block:
            exclude_ids = exclude_block[rk]

        resource = RESOURCE_TYPE_OBJECT_MAP[rk](options=opts, validate=validate, exclude=exclude_ids)
            
        out.append(resource)


    return out
