from constants import ALL_RESOURCE_TYPES
from exceptions import InvalidResourceTypeError

"""
Resource config structure
{
    "resource_type" {
        "option_key": "option_val"
    }
}

"""

def parse_config_file(jsonString):
    for k in jsonString:
        if k not in ALL_RESOURCE_TYPES:
            raise InvalidResourceTypeError(f"invalid resource type: {k}")
        
    
    
        
        
