"""
handles all hcl related operations
"""

from typing import List
from .dataclasses import SingleItem

def import_block(resource_type, jpro_id):
    """
    Return a Terraform import block string for a resource.
    """

    return (
        f"import {{\n"
        f"  id = {jpro_id}\n"
        f"  to = {resource_type.value}.{resource_type.value}-{jpro_id}\n"
        f"}}\n"
    )


def generate_imports(resources: List[SingleItem]) -> list:
    """
    Return import blocks for a list of SingleItem resources.
    """

    return [import_block(i.resource_type, i.jpro_id) for i in resources]
