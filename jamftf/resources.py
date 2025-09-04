"""Resource parent object."""

from .models import Resource
from .enums import ProviderResourceTags, ResourceResponseKeys

__all__ = [
    "Scripts",
    "Categories",
    "Policies",
    "ConfigurationProfiles",
    "ComputerGroupsStatic",
    "ComputerGroupsSmart",
    "AdvancedComputerSearches",
    "ComputerExtensionAttributes",
]


class Scripts(Resource):
    """Jamf Pro script resource."""
    resource_type = ProviderResourceTags.SCRIPT

    def _get(self):
        self._get_from_api(
            self.client.classic.scripts.get_all,
            ResourceResponseKeys.SCRIPTS,
        )


class Categories(Resource):
    """Jamf Pro category resource."""
    resource_type = ProviderResourceTags.CATEGORY

    def _get(self):
        self._get_from_api(
            self.client.classic.categories.get_all,
            ResourceResponseKeys.CATEGORIES,
        )


class Policies(Resource):
    """Jamf Pro policy resource."""
    resource_type = ProviderResourceTags.POLICY

    def _get(self):
        self._get_from_api(
            self.client.classic.policies.get_all,
            ResourceResponseKeys.POLICIES,
        )


class ConfigurationProfiles(Resource):
    """macOS configuration profile resource."""
    resource_type = ProviderResourceTags.MACOS_CONFIG_PROFILE

    def _get(self):
        self._get_from_api(
            self.client.classic.configuration_profiles.get_all,
            ResourceResponseKeys.CONFIG_PROFILES,
        )


class ComputerGroupsStatic(Resource):
    """Static computer group resource."""
    resource_type = ProviderResourceTags.COMPUTER_GROUP_STATIC

    def _get(self):
        self._get_from_api(
            self.client.classic.computer_groups.get_all,
            ResourceResponseKeys.COMPUTER_GROUPS,
            filter_fn=lambda i: not i["is_smart"],
        )


class ComputerGroupsSmart(Resource):
    """Smart computer group resource."""
    resource_type = ProviderResourceTags.COMPUTER_GROUP_SMART

    def _get(self):
        self._get_from_api(
            self.client.classic.computer_groups.get_all,
            ResourceResponseKeys.COMPUTER_GROUPS,
            filter_fn=lambda i: i["is_smart"],
        )


class AdvancedComputerSearches(Resource):
    """Advanced computer search resource."""
    resource_type = ProviderResourceTags.ADVANCED_COMPUTER_SEARCH

    def _get(self):
        self._get_from_api(
            self.client.classic.computer_searches.get_all,
            ResourceResponseKeys.ADVANCED_COMPUTER_SEARCHES,
        )


class ComputerExtensionAttributes(Resource):
    """Computer extension attribute resource."""
    resource_type = ProviderResourceTags.COMPUTER_EXT_ATTR

    def _get(self):
        self._get_from_api(
            self.client.classic.computer_extension_attributes.get_all,
            ResourceResponseKeys.EXT_ATTRS,
        )
