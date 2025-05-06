"""Configuration file ingest functions"""

from typing import List
import json
from .constants import valid_resource_key, RESOURCE_TYPE_OBJECT_MAP
from .exceptions import InvalidResourceTypeError
from .models import Resource

def parse_config_file(path: str) -> list[Resource]:

    json_data = {}
    with open(path, "r", encoding="UTF-8") as f:
        json_data = json.load(f)


    return parse_config_dict(json_data)


def parse_config_dict(config_json: dict) -> List[Resource]:
    out = []

    for res_key, active in config_json.items():

        if not valid_resource_key(res_key):
            raise InvalidResourceTypeError(f"invalid resource type: {res_key}")

        if not active:
            continue

        out.append(
            RESOURCE_TYPE_OBJECT_MAP[res_key]()
        )

    return out
