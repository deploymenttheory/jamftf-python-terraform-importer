
# Vars
ILLEGAL_NAME_CHARS = [".", "/"]

# terraform resource type strings centralised
RESOURCE_TYPES = {
    "scripts": "jamfpro_script",
    "categories": "jamfpro_categorie",
    "departments": "jamfpro_department"
}

ALL_RESOURCE_TYPES = list(RESOURCE_TYPES.values())