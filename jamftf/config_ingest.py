"""manages configuration injest"""

from typing import List
from .constants import (
    EXCLUDE_BLOCK_CONFIG_KEY,
    ALL_RESOURCE_TYPES,
    RESOURCE_BLOCK_CONFIG_KEY,
    VALID_RESOURCE_CONFIG_KEYS,
    REQUIRED_RESOURCE_CONFIG_KEYS
)
from .exceptions import InvalidResourceTypeError, DataError
from .resources import (
    Resource,
    Scripts,
    Categories,
    Policies
)
from .options import Options

import json


RESOURCE_TYPE_OBJECT_MAP = {
    "jamfpro_script": Scripts,
    "jamfpro_category": Categories,
    "jamfpro_policy": Policies
}


def parse_config_file(path: str) -> list[Resource]:
    """
    Parse a configuration file and return a list of Resource objects.

    This function processes a filepath, extracting resource
    definitions and any exclusion rules. It performs validation on the configuration
    structure and creates Resource objects based on the provided specifications.

    Args:
        path (string): A dictionary containing the configuration data.

    Returns:
        List[Resource]: A list of instantiated Resource objects.

    Raises:
        KeyError: If the required resources block is missing from the config.
        DataError: If there are invalid keys or missing required keys in the config.
        InvalidResourceTypeError: If an invalid resource type is specified.

    The function expects the following structure in the config_json:
    - An optional 'exclude_block' key for specifying resources to exclude.
    - A required 'resources' key containing resource definitions.

    Each resource definition should include 'active', 'validate', and other
    required keys as specified in REQUIRED_RESOURCE_CONFIG_KEYS.
    """

    # Validate the path here
    sanitized_path = path

    jsonData = {}
    with open(sanitized_path, "w") as f:
        jsonData = json.load(f)


    return parse_config_dict(jsonData)


def parse_config_dict(config_json: dict) -> List[Resource]:
    """
    Parse a configuration file and return a list of Resource objects.

    This function processes a JSON configuration dictionary, extracting resource
    definitions and any exclusion rules. It performs validation on the configuration
    structure and creates Resource objects based on the provided specifications.

    Args:
        config_json (dict): A dictionary containing the configuration data.

    Returns:
        List[Resource]: A list of instantiated Resource objects.

    Raises:
        KeyError: If the required resources block is missing from the config.
        DataError: If there are invalid keys or missing required keys in the config.
        InvalidResourceTypeError: If an invalid resource type is specified.

    The function expects the following structure in the config_json:
    - An optional 'exclude_block' key for specifying resources to exclude.
    - A required 'resources' key containing resource definitions.

    Each resource definition should include 'active', 'validate', and other
    required keys as specified in REQUIRED_RESOURCE_CONFIG_KEYS.
    """
    out = []
    exclude_block = {}

    if EXCLUDE_BLOCK_CONFIG_KEY in config_json:
        exclude_block = config_json[EXCLUDE_BLOCK_CONFIG_KEY]

        for rk in exclude_block:
            if rk not in ALL_RESOURCE_TYPES:
                raise DataError("invalid resource key in exclude block")


    if RESOURCE_BLOCK_CONFIG_KEY not in config_json:
        raise KeyError("resources block not present in config file")

    print(config_json[RESOURCE_BLOCK_CONFIG_KEY].values())
    for k, v in config_json[RESOURCE_BLOCK_CONFIG_KEY].values():

        if k not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {k}")

        for i in v:
            if i not in VALID_RESOURCE_CONFIG_KEYS:
                raise DataError(f"invalid config key: {i}")

        for i in REQUIRED_RESOURCE_CONFIG_KEYS:
            if i not in v:
                raise DataError(f"missing required config key: {i}")
            
        assert isinstance(v["validate"], bool), "validate key is not a bool"
        assert isinstance(v["active"], bool), "active key is not a bool"

        if not v["active"]:
            continue

        out.append(
            RESOURCE_TYPE_OBJECT_MAP[rk](
                options=Options().from_json(v), 
                validate=v["validate"], 
                exclude=exclude_block[rk] if rk in exclude_block else []
            )
        )

    return out
