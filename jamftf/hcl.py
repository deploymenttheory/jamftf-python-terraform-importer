"""
handles all hcl related operations
"""

def import_block(resource_type, name, id):
    """
    Constructs a valid import block using the resource type, name and server id.
    """

    return "import {\nid = " + str(id) + "\nto = " + f"{resource_type}.{name}" + "\n}" 


def generate_imports(data: dict) -> list:
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

    for d in data["resources"]:
        out_list.append(
            import_block(
                resource_type=data["resource_type"],
                name = data["resources"][d]["name"],
                id = data[d]["resources"]["id"]
            )
        )

    return out_list
