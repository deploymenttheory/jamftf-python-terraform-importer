"""Configuration file ingest functions"""

from typing import List
import json
from .constants import (
    ALL_RESOURCE_TYPES,
    RESOURCE_BLOCK_CONFIG_KEY,
    VALID_RESOURCE_CONFIG_KEYS,
    REQUIRED_RESOURCE_CONFIG_KEYS,
    valid_resource_key
)
from .exceptions import InvalidResourceTypeError, DataError
from .resources import (
    Resource,
    Scripts,
    Categories,
    Policies,
    ConfigurationProfiles,
    ComputerGroupsStatic,
    ComputerGroupsSmart,
    AdvancedComputerSearches,
    ComputerExtensionAttributes
)
from .options import Options


RESOURCE_TYPE_OBJECT_MAP = {
    "jamfpro_script": Scripts,
    "jamfpro_category": Categories,
    "jamfpro_policy": Policies,
    "jamfpro_macos_configuration_profile_plist": ConfigurationProfiles,
    "jamfpro_static_computer_group": ComputerGroupsStatic,
    "jamfpro_smart_computer_group": ComputerGroupsSmart,
    "jamfpro_advanced_computer_search": AdvancedComputerSearches,
    "jamfpro_computer_extension_attribute": ComputerExtensionAttributes
}


def parse_config_file(path: str) -> list[Resource]:

    json_data = {}
    with open(path, "r", encoding="UTF-8") as f:
        json_data = json.load(f)


    return parse_config_dict(json_data)


def parse_config_dict(config_json: dict) -> List[Resource]:
    out = []

    # for res key, keys
    for res_key, active in config_json.items():

        # If invalid resource
        if not valid_resource_key(res_key):
            raise InvalidResourceTypeError(f"invalid resource type: {res_key}")

        # If inactive, skip
        if not active:
            continue

        out.append(
            RESOURCE_TYPE_OBJECT_MAP[res_key]()
        )

    return out
