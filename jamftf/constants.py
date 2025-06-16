"""Storage for all constant values for easier configuration."""

from .enums import ProviderResourceTags
from .resources import (
    Scripts,
    Categories,
    Policies,
    ConfigurationProfiles,
    ComputerGroupsStatic,
    ComputerGroupsSmart,
    AdvancedComputerSearches,
    ComputerExtensionAttributes,
)

__all__ = [
    "ProviderResourceTags",
    "RESOURCE_TYPE_OBJECT_MAP",
    "valid_resource_key",
]

# Map from config file keys to resource types
RESOURCE_KEY_MAP = {
    "scripts": ProviderResourceTags.SCRIPT,
    "categories": ProviderResourceTags.CATEGORY,
    "policies": ProviderResourceTags.POLICY,
    "configuration_profiles": ProviderResourceTags.MACOS_CONFIG_PROFILE,
    "computer_groups_static": ProviderResourceTags.COMPUTER_GROUP_STATIC,
    "computer_groups_smart": ProviderResourceTags.COMPUTER_GROUP_SMART,
    "advanced_computer_searches": ProviderResourceTags.ADVANCED_COMPUTER_SEARCH,
    "computer_extension_attributes": ProviderResourceTags.COMPUTER_EXT_ATTR,
}

RESOURCE_TYPE_OBJECT_MAP = {
    ProviderResourceTags.SCRIPT: Scripts,
    ProviderResourceTags.CATEGORY: Categories,
    ProviderResourceTags.POLICY: Policies,
    ProviderResourceTags.MACOS_CONFIG_PROFILE: ConfigurationProfiles,
    ProviderResourceTags.COMPUTER_GROUP_STATIC: ComputerGroupsStatic,
    ProviderResourceTags.COMPUTER_GROUP_SMART: ComputerGroupsSmart,
    ProviderResourceTags.ADVANCED_COMPUTER_SEARCH: AdvancedComputerSearches,
    ProviderResourceTags.COMPUTER_EXT_ATTR: ComputerExtensionAttributes,
}

def valid_resource_key(key: str) -> bool:
    """Check if the key is a valid resource type in the config file."""
    return key in RESOURCE_KEY_MAP
