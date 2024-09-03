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
    exclude = {}

    if "exclude_ids" in config_json:
        exclude = config_json["exclude_ids"]

        for rk in exclude:
            if rk not in ALL_RESOURCE_TYPES:
                raise DataError("invalid resource key in exclude block")
            
    if "resources" not in config_json:
        raise KeyError("resources block not present in config file")


    resources = config_json["resources"]
    for r in resources:

        # Validation
        # Valid Resource Types only
        # Valid option keys
        # Required keys not missing
        # Skips inactive resources

        if r not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {r}")

        for i in resources[r]:
            if i not in VALID_CONFIG_KEYS:
                raise DataError(f"invalid config key: {i}")
        
        for i in REQUIRED_CONFIG_FLAGS:
            if i not in resources[r]:
                raise DataError(f"missing required config key: {i}")

        if not resources[r]["active"]:
            continue

        opts = Options().from_json(resources[r])
        validate = config_json[r][validate]
        assert isinstance(validate, bool), "validate key is not a bool"

        resource: Resource
        resource = RESOURCE_TYPE_OBJECT_MAP[r](options=opts, validate=validate)

        if r in exclude:
            resource.set_exclude(exclude[r])
            
        out.append(resource)


    exclude = config_json["exclude_ids"]


    return out
