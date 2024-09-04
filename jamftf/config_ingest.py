"""Configuration file ingest functions"""

from typing import List
import json
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

    # // TODO sanitise  the path
    sanitized_path = path

    json_data = {}
    with open(sanitized_path, "r", encoding="UTF-8") as f:
        json_data = json.load(f)


    return parse_config_dict(json_data)


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


    res_block: dict = config_json[RESOURCE_BLOCK_CONFIG_KEY]
    k: str
    v: dict
    for k, v in res_block.items():

        if k not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {k}")

        for i in v:
            if i not in VALID_RESOURCE_CONFIG_KEYS:
                raise DataError(f"invalid config key: {i}")

        for i in REQUIRED_RESOURCE_CONFIG_KEYS:
            if i not in v:
                raise DataError(f"missing required config key: {i}")

        validate = v["validate"]
        if not isinstance(validate, bool):
            raise AssertionError(f"validate key is of the wrong type: {validate}, {type(validate)}")

        active = v["active"]
        if not isinstance(active, bool):
            raise AssertionError(f"active key is of the wrong type: {active}, {type(active)}")

        if not active:
            continue

        out.append(
            RESOURCE_TYPE_OBJECT_MAP[k](
                options=Options().from_json(v),
                validate=validate,
                exclude=exclude_block[k] if k in exclude_block else []
            )
        )

    return out
