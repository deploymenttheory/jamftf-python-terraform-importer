"""storage for all constant values for easier configuration"""

# Vars
ILLEGAL_NAME_CHARS = [".", "/", " "]

# terraform resource type strings centralised
RESOURCE_TYPES = {
    "script": "jamfpro_script",
    "category": "jamfpro_category",
    "department": "jamfpro_department",
    "policy": "jamfpro_policy",
    "osx_config_profile": "jamfpro_macos_configuration_profile_plist"
}

ALL_RESOURCE_TYPES = list(RESOURCE_TYPES.values())

