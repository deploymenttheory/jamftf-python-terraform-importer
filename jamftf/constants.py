
# Vars
ILLEGAL_NAME_CHARS = [".", "/"]

# terraform resource type strings centralised
RESOURCE_TYPES = {
    "script": "jamfpro_script",
    "category": "jamfpro_categorie",
    "department": "jamfpro_department"
}

ALL_RESOURCE_TYPES = list(RESOURCE_TYPES.values())