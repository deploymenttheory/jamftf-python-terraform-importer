"""storage for all constant values for easier configuration"""

# Invalid characters in resource names
ILLEGAL_NAME_CHARS = [".", "/", " "]

# terraform resource type strings centralised
RESOURCE_TYPES = {
    "script": "jamfpro_script",
    "category": "jamfpro_category",
    "department": "jamfpro_department",
    "policy": "jamfpro_policy",
    "osx_config_profile": "jamfpro_macos_configuration_profile_plist"
}

# Values from above
ALL_RESOURCE_TYPES = list(RESOURCE_TYPES.values())

# Required keys in every resource config block
REQUIRED_RESOURCE_CONFIG_KEYS = [
    "active",
    "validate"
]

# All balid config keys
VALID_RESOURCE_CONFIG_KEYS = [
    "active", 
    "validate",
    "use_resource_type_as_name",
    "exclude_ids",
]

# Config keys in one place
EXCLUDE_BLOCK_CONFIG_KEY = "exclude_ids"
RESOURCE_BLOCK_CONFIG_KEY = "resources"
