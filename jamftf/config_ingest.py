"""Configuration file ingest functions"""

from pathlib import Path
from typing import List
import json
from .constants import valid_resource_key, RESOURCE_TYPE_OBJECT_MAP
from .exceptions import InvalidResourceTypeError
from .models import Resource


def parse_config_file(path: str) -> list[Resource]:
    """
    Loads and parses a JSON config file from the given path into Resource objects.

    The path is sanitized, expanded, and validated before reading.
    Raises FileNotFoundError if the file does not exist.
    """

    safe_path = Path(path).expanduser().resolve(strict=False)

    if not safe_path.is_file():
        raise FileNotFoundError(f"Config file not found: {safe_path}")

    with safe_path.open("r", encoding="UTF-8") as f:
        json_data = json.load(f)

    return parse_config_dict(json_data)


def parse_config_dict(config_json: dict) -> List[Resource]:
    """
    Parses a config dictionary into a list of active Resource instances.

    Skips inactive entries and raises InvalidResourceTypeError for unknown resource types.
    """

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
