"""
handles all hcl related operations
"""

SPACE = "\x20"

from typing import List
from .dataclasses import SingleItem

def import_block(resource_type, jpro_id):
    """
    Return a Terraform import block string for a resource.
    """

    # Unsure if I'm a fan of how these strings are constructed but it improves clarity
    # on exactly which characters are being returned and how many of them.
    return (
        f"import {{\n"
        f"{2 * SPACE}id{SPACE}={SPACE}{jpro_id}\n"
        f"{2 * SPACE}to{SPACE}={SPACE}{resource_type.value}.{resource_type.value}-{jpro_id}\n"
        f"}}\n"
    )


def generate_imports(resources: List[SingleItem]) -> list:
    """
    Return import blocks for a list of SingleItem resources.
    """

    return [import_block(i.resource_type, i.jpro_id) for i in resources]
