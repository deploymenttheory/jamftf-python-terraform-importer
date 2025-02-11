"""Resource parent object"""

from logging import Logger
import jamfpy
from requests import HTTPError
from .options import Options, Applicator
from .exceptions import (
    InvalidResourceTypeError,
    ImporterConfigError
)
from .hcl import generate_imports
from .constants import RESOURCE_TYPES


class Resource:
    """parent obj for resources"""
    resource_type = ""
    lg: Logger

    def __init__(
            self,
            options: Options = None,
            validate: bool = True,
            client: jamfpy.Tenant = None,
            debug: bool = False,
            exclude: list[int] = None
        ):

        self._validate_resource_type()

        log_level = self._init_log_level(debug)
        self._init_logger(log_level)

        self.data = {}
        self.client = client
        self.exclude = exclude

        self.options = options if options is not None else Options()
        self._init_applicator(log_level, validate)



        self.lg.info("resource initilized: %s", self.resource_type)


    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"


    # Private

    def _init_applicator(self, log_level, validate):
        """init_applicator initilizes an applicator and adds a logger"""
        logger = jamfpy.get_logger(f"applicator({self.resource_type})", level=log_level)
        self.applicator = Applicator(
            self.resource_type,
            opts=self.options.options(),
            validate=validate,
            logger=logger,
            exclude_ids=self.exclude
        )


    def _init_logger(self, log_level: int):
        """_init_logger initilizes a logger"""
        self.lg = jamfpy.get_logger(f"resource-{self.resource_type}", level=log_level)


    def _init_log_level(self, debug: bool) -> int:
        """init logging implements a simple two level logging approach"""

        assert isinstance(debug, bool), "debug flag is not bool"

        log_levels = {
            "True": 10,
            "False": 20,
        }

        return log_levels[str(debug)]


    def _validate_resource_type(self):
        """_validate_resource_type validates that the resource type parameter is set"""
        if not self.resource_type:
            raise InvalidResourceTypeError(f"Instantiate a specific resource type and not the parent {self.resource_type}")


    def apply_options(self):
        """sends data through applicator object to have options applied""" 
        self.lg.debug("applying options...")
        self.data = self.applicator.apply(self.data)


    def _log_get(self):
        """standardises log for getting data"""
        self.lg.info("getting data for resource type: %s", self.resource_type)


    def _get(self):
        """
        Retrieves data from api and should always populate self.data with:
        {
            "jamfpro_resourcename.id": {
                "id": X,
                "name": Y
            }
        }
        """


        raise ImporterConfigError("operation invalid at Resource level. Please define a resource type")


    # Public

    def set_debug(self, debug: bool):
        """overrides log level to debug for all handlers, including the applicator"""
        level = self._init_log_level(debug)

        self.lg.setLevel(level)
        for i in self.lg.handlers:
            i.setLevel(level)

        self.applicator.lg.setLevel(level)
        for i in self.applicator.lg.handlers:
            i.setLevel(level)

        self.lg.info("log level has been overridden to: %s", self.lg.level)


    def set_client(self, client: jamfpy.Tenant, refresh_data: bool = False):
        """function to wrap setting of object bound client"""
        self.lg.debug("setting client...")

        assert isinstance(client, jamfpy.Tenant), "invalid client type"
        self.lg.debug("client type is correct")

        self.client = client
        self.lg.debug("client set successfully")

        if refresh_data:
            self.refresh_data()


    def set_options(self, options: Options, apply: bool = True):
        """set_options allows options to be set after instantiation"""
        self.lg.debug("setting options...")

        assert isinstance(options, Options)
        self.lg.debug("options type is correct")


        self.options = options
        self.lg.debug("options set successfully")

        if apply:
            self.apply_options()


    def refresh_data(self):
        """refreshes data held by object from api"""
        self.lg.info("refreshing data...")

        if self.client is None:
            raise ImporterConfigError("no client provided. Provide client via object creation or .set_client(client)")

        self._get()
        self.apply_options()


    def build_hcl(self):
        """Generates HCL for all Script attrs"""
        return generate_imports(self.resource_type, self.data)


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

        resp, data = self.client.pro.scripts.get_all()
        if not resp.ok:
            raise HTTPError("bad api call")

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
    resource_type = RESOURCE_TYPES["computer_group_static"]

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