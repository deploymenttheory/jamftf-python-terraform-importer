"""storage for all constant values for easier configuration"""
from .resources import (
    Scripts,
    Categories,
    Policies,
    ConfigurationProfiles,
    ComputerGroupsStatic,
    ComputerGroupsSmart,
    AdvancedComputerSearches,
    ComputerExtensionAttributes
)

from enum import Enum

class ProviderResourceTags(str, Enum):
    script = "jamfpro_script"
    category = "jamfpro_category"
    policy = "jamfpro_policy"
    macos_config_profile = "jamfpro_macos_configuration_profile_plist"
    computer_group_static = "jamfpro_static_computer_group"
    computer_group_smart = "jamfpro_smart_computer_group"
    advanced_computer_search = "jamfpro_advanced_computer_search"
    computer_ext_attr = "jamfpro_computer_extension_attribute"

    @classmethod
    def all(cls):
        return list(cls)

    @classmethod
    def valid_resource_check(cls, key: str):
        return key in cls._value2member_map_


RESOURCE_TYPE_OBJECT_MAP = {
    ProviderResourceTags.script: Scripts,
    ProviderResourceTags.category: Categories,
    ProviderResourceTags.policy: Policies,
    ProviderResourceTags.macos_config_profile: ConfigurationProfiles,
    ProviderResourceTags.computer_group_static: ComputerGroupsStatic,
    ProviderResourceTags.computer_group_smart: ComputerGroupsSmart,
    ProviderResourceTags.advanced_computer_search: AdvancedComputerSearches,
    ProviderResourceTags.computer_ext_attr: ComputerExtensionAttributes
}


def valid_resource_key(key):
    return ProviderResourceTags.valid_resource_check(key)