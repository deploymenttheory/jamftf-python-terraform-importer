from constants import ALL_RESOURCE_TYPES, RESOURCE_TYPE_OBJECTS
from exceptions import InvalidResourceTypeError
from typing import List
from .resources.resources import Resource

"""
Resource config structure
{
    "resource_type" {
        "option_key": "option_val"
    }
}

"""




def parse_config_file(jsonString) -> List[Resource]:
    out = []
    for k in jsonString:
        if k not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {k}")
        
        out.append(RESOURCE_TYPE_OBJECTS[k])
    

    return out
    
        
        
