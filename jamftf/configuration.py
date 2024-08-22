from typing import List

from .constants import ALL_RESOURCE_TYPES
from .exceptions import *
from .resources.resources import *


"""
Resource config structure
{
    "resource_type" {
        "option_key": "option_val"
    }
}

"""

RESOURCE_TYPE_OBJECT_MAP = {
    "jamfpro_script": Scripts,
    "jamfpro_category": Categories
}




VALID_CONFIG_KEYS = ["active"]
REQUIRED_CONFIG_KEYS = ["active"]

def parse_config_file(configJson: dict) -> List[Resource]:
    out = []

    for rk in configJson:

        # Invalid resource key
        if rk not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {rk}")
        
        # Invalid option key
        if not all(i in VALID_CONFIG_KEYS for i in configJson[rk]):
            raise DataError(f"invalid options key found")

        # Resource not set to active
        if not configJson[rk]["active"]:
            continue

        # for opt in configJson[rk]:



    return out
    
        
