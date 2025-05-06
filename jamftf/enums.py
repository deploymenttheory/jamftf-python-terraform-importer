"""Storage for enums"""

from enum import Enum

class ProviderResourceTags(str, Enum):
    """Supported Jamf provider resource tags."""

    SCRIPT = "jamfpro_script"
    CATEGORY = "jamfpro_category"
    POLICY = "jamfpro_policy"
    MACOS_CONFIG_PROFILE = "jamfpro_macos_configuration_profile_plist"
    COMPUTER_GROUP_STATIC = "jamfpro_static_computer_group"
    COMPUTER_GROUP_SMART = "jamfpro_smart_computer_group"
    ADVANCED_COMPUTER_SEARCH = "jamfpro_advanced_computer_search"
    COMPUTER_EXT_ATTR = "jamfpro_computer_extension_attribute"

    @classmethod
    def all(cls) -> list["ProviderResourceTags"]:
        """Return all enum members."""
        return list(cls)

    @classmethod
    def valid_resource_check(cls, key: str) -> bool:
        """Return True if key is a valid enum value."""
        try:
            cls(key)
        except ValueError:
            return False
        return True


class ResourceResponseKeys(str, Enum):
    """Top-level JSON keys for each Jamf Pro resource API response."""
    SCRIPTS = "scripts"
    CATEGORIES = "categories"
    POLICIES = "policies"
    CONFIG_PROFILES = "os_x_configuration_profiles"
    COMPUTER_GROUPS = "computer_groups"
    ADVANCED_COMPUTER_SEARCHES = "advanced_computer_searches"
    EXT_ATTRS = "computer_extension_attributes"
