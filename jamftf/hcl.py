"""
handles all hcl related operations
"""

def import_block(resource_type, name, jpro_id):
    """
    Generate a formatted import block for a resource.

    Args:
        resource_type (str): The type of the resource being imported.
        name (str): The name of the resource.
        jpro_id (int or str): The server ID of the resource.

    Returns:
        str: A formatted string representing the import block.

    Example:
        >>> import_block("aws_instance", "web_server", 12345)
        "import {
        id = 12345
        to = aws_instance.web_server
        }
        "
    """

    return "import {\nid = " + str(jpro_id) + "\nto = " + f"{resource_type}.{name}" + "\n}\n"


def generate_imports(resource_type: str, resources: dict) -> list:
    """
    todo
    """
    out_list = []

    for d in resources:
        out_list.append(
            import_block(
                resource_type=resource_type,
                name = resources[d]["name"],
                jpro_id = resources[d]["id"]
            )
        )

    return out_list
