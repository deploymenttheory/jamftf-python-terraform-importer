"""Resource parent object."""

from requests import HTTPError
from .models import Resource
from .constants import ProviderResourceTags


class Scripts(Resource):
    """Jamf Pro script resource."""
    resource_type = ProviderResourceTags.SCRIPT

    def _get(self):
        """Fetch and populate script data."""
        self._log_get()

        resp = self.client.classic.scripts.get_all()
        resp.raise_for_status()

        for i in resp.json()["scripts"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class Categories(Resource):
    """Jamf Pro category resource."""
    resource_type = ProviderResourceTags.CATEGORY

    def _get(self):
        """Fetch and populate category data."""
        self._log_get()

        resp = self.client.classic.categories.get_all()
        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["categories"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class Policies(Resource):
    """Jamf Pro policy resource."""
    resource_type = ProviderResourceTags.POLICY

    def _get(self):
        """Fetch and populate policy data."""
        self._log_get()

        resp = self.client.classic.policies.get_all()
        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["policies"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class ConfigurationProfiles(Resource):
    """macOS configuration profile resource."""
    resource_type = ProviderResourceTags.MACOS_CONFIG_PROFILE

    def _get(self):
        """Fetch and populate configuration profile data."""
        self._log_get()

        resp = self.client.classic.configuration_profiles.get_all()
        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["os_x_configuration_profiles"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class ComputerGroupsStatic(Resource):
    """Static computer group resource."""
    resource_type = ProviderResourceTags.COMPUTER_GROUP_STATIC

    def _get(self):
        """Fetch and populate static computer group data."""
        self._log_get()

        resp = self.client.classic.computergroups.get_all()
        resp.raise_for_status()

        for i in resp.json()["computer_groups"]:
            if not i["is_smart"]:
                self.data[f"{i['name']}.{i['id']}"] = {
                    "id": i["id"],
                    "name": i["name"],
                }


class ComputerGroupsSmart(Resource):
    """Smart computer group resource."""
    resource_type = ProviderResourceTags.COMPUTER_GROUP_SMART

    def _get(self):
        """Fetch and populate smart computer group data."""
        self._log_get()

        resp = self.client.classic.computergroups.get_all()
        resp.raise_for_status()

        for i in resp.json()["computer_groups"]:
            if i["is_smart"]:
                self.data[f"{i['name']}.{i['id']}"] = {
                    "id": i["id"],
                    "name": i["name"],
                }


class AdvancedComputerSearches(Resource):
    """Advanced computer search resource."""
    resource_type = ProviderResourceTags.ADVANCED_COMPUTER_SEARCH

    def _get(self):
        """Fetch and populate advanced computer search data."""
        self._log_get()

        resp = self.client.classic.computer_searches.get_all()
        resp.raise_for_status()

        for i in resp.json()["advanced_computer_searches"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class ComputerExtensionAttributes(Resource):
    """Computer extension attribute resource."""
    resource_type = ProviderResourceTags.COMPUTER_EXT_ATTR

    def _get(self):
        """Fetch and populate computer extension attribute data."""
        self._log_get()

        resp = self.client.classic.computer_extension_attributes.get_all()
        resp.raise_for_status()

        for i in resp.json()["computer_extension_attributes"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }
