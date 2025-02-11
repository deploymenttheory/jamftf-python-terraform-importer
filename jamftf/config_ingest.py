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
    Policies,
    ConfigurationProfiles,
    ComputerGroupsStatic,
    ComputerGroupsSmart
)
from .options import Options


RESOURCE_TYPE_OBJECT_MAP = {
    "jamfpro_script": Scripts,
    "jamfpro_category": Categories,
    "jamfpro_policy": Policies,
    "jamfpro_macos_configuration_profile_plist": ConfigurationProfiles,
    "jamfpro_static_computer_group": ComputerGroupsStatic,
    "jamfpro_smart_computer_group": ComputerGroupsSmart

}


def parse_config_file(path: str) -> list[Resource]:

    json_data = {}
    with open(path, "r", encoding="UTF-8") as f:
        json_data = json.load(f)


    return parse_config_dict(json_data)


def parse_config_dict(config_json: dict) -> List[Resource]:

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

    # for res key, keys
    for k, v in res_block.items():

        # If invalid resource
        if k not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {k}")

        # If it contains an invalid config key
        for i in v:
            if i not in VALID_RESOURCE_CONFIG_KEYS:
                raise DataError(f"invalid config key: {i}")

        # If missing a required config key
        for i in REQUIRED_RESOURCE_CONFIG_KEYS:
            if i not in v:
                raise DataError(f"missing required config key: {i}")

        # If the resource should be validated
        validate = v["validate"]
        if not isinstance(validate, bool):
            raise AssertionError(f"validate key is of the wrong type: {validate}, {type(validate)}")

        # If the resource should be prossessed.
        active = v["active"]
        if not isinstance(active, bool):
            raise AssertionError(f"active key is of the wrong type: {active}, {type(active)}")

        # If inactive, skip
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
