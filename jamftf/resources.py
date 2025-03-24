"""Resource parent object"""

from logging import Logger
import jamfpy
from requests import HTTPError
from .options import Options, Applicator
from .exceptions import (
    InvalidResourceTypeError,
    ImporterConfigError
)
from .models import Resource
from .constants import RESOURCE_TYPES




class Scripts(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPES["script"]

    def _get(self):
        """
        Retrieves data from api and should always populate self.data with:
        {
            "name.id": {
                "id": id,
                "name": name
            }
        }
        """
        self._log_get()

        resp = self.client.classic.scripts.get_all()
        resp.raise_for_status()

        data = resp.json()["scripts"]
        for i in data:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class Categories(Resource):
    """categories"""
    resource_type = RESOURCE_TYPES["category"]

    def _get(self):
        self._log_get()

        resp = self.client.classic.categories.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["categories"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"]
            }


class Policies(Resource):
    """policies"""
    resource_type = RESOURCE_TYPES["policy"]

    def _get(self):
        self._log_get()

        resp = self.client.classic.policies.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["policies"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"]
            }


class ConfigurationProfiles(Resource):
    """osx config profile"""
    resource_type = RESOURCE_TYPES["osx_config_profile"]

    def _get(self):
        self._log_get()

        resp = self.client.classic.configuration_profiles.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["os_x_configuration_profiles"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"]
            }


class ComputerGroupsStatic(Resource):
    resource_type = RESOURCE_TYPES["computer_group_static"]

    def _get(self):
        self._log_get()

        resp = self.client.classic.computergroups.get_all()

        resp.raise_for_status()

        for i in resp.json()["computer_groups"]:
            if not i["is_smart"]:
                self.data[f"{i["name"]}.{i["id"]}"] = {
                    "id": i["id"],
                    "name": i["name"]
                }


class ComputerGroupsSmart(Resource):
    resource_type = RESOURCE_TYPES["computer_group_smart"]

    def _get(self):
        self._log_get()

        resp = self.client.classic.computergroups.get_all()

        resp.raise_for_status()

        for i in resp.json()["computer_groups"]:
            if i["is_smart"]:
                self.data[f"{i["name"]}.{i["id"]}"] = {
                    "id": i["id"],
                    "name": i["name"]
                }


class AdvancedComputerSearches(Resource):
    resource_type = RESOURCE_TYPES["advanced_computer_search"]

    def _get(self):
        self._log_get()

        resp = self.client.classic.computer_searches.get_all()

        resp.raise_for_status()

        for i in resp.json()["advanced_computer_searches"]:
                self.data[f"{i["name"]}.{i["id"]}"] = {
                    "id": i["id"],
                    "name": i["name"]
                }

class ComputerExtensionAttributes(Resource):
    resource_type = RESOURCE_TYPES["computer_ext_attr"]
    
    def _get(self):
        self._log_get()

        resp = self.client.classic.computer_extension_attributes.get_all()
        
        resp.raise_for_status()

        for i in resp.json()["computer_extension_attributes"]:
                self.data[f"{i["name"]}.{i["id"]}"] = {
                    "id": i["id"],
                    "name": i["name"]
                }