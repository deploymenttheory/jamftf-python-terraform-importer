"""Handles all HCL related operations."""

from .dataclasses import SingleItem

def get_resource_name(resource_name: str, jpro_id: str) -> str:
    """Generate a descriptive name for a resource."""
    
    the_resource_name = ''.join(c if c.isalpha() else '_' for c in resource_name)
    # Convert to camelCase
    type_name = the_resource_name.lower()
    return f"{type_name}{jpro_id}"

def resource_block(resource_type: str, resource_name: str, jpro_id: str) -> str:
    """Generate a resource block for a resource."""
    name = get_resource_name(resource_name, jpro_id)
    return f'resource "{resource_type}" "{name}" {{\n  name = "{resource_name}" \n}}'

def import_block(resource_type: str, resource_name: str, jpro_id: str) -> str:
    """Generate an import block for a resource."""
    name = get_resource_name(resource_name, jpro_id)
    return f'import {{\n  to = {resource_type}.{name}\n  id = "{jpro_id}"\n}}'

def generate_imports(items: list[SingleItem]) -> str:
    """Generate resource and import blocks for a list of resources."""
    blocks = []
    for item in items:
         # Then add import block
        blocks.append(import_block(item.resource_type.value, item.resource_name, item.jpro_id))
        
        # Add resource block first
        blocks.append(resource_block(item.resource_type.value, item.resource_name, item.jpro_id))
       
        # Add blank line between resource groups
        blocks.append("")
    return "\n".join(blocks)
