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
    """Check if the key is a valid provider resource tag."""
    return ProviderResourceTags.valid_resource_check(key)
