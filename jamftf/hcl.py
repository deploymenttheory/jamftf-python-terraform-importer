"""
handles all hcl related operations
"""

def import_block(resource_type, name, jpro_id):
    """
    Constructs a valid import block using the resource type, name and server id.
    """

    return "import {\n\tid = " + str(jpro_id) + "\n\tto = " + f"{resource_type}.{name}" + "\n}\n"


def generate_imports(resource_type: str, resources: dict) -> list:
    """
    Generates multiple 
    data should follow this structure:
    data: {
        "resource_type": TYPE AS IN PROVIDER
        "resources": {
            "name.id": {
                "id": X
                "name": Y
            },
            "name2.id": {
                "id": X
                "name": Y
            }
        }
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
