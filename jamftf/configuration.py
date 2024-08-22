from typing import List

from .constants import ALL_RESOURCE_TYPES
from .exceptions import InvalidResourceTypeError
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
    "jamfpro_catagory": Categories
}


def parse_config_file(configJson) -> List[Resource]:
    out = []

    for k in configJson:
        if k not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {k}")
        
        out.append(RESOURCE_TYPE_OBJECT_MAP[k])
    

    return out
    
        
        
