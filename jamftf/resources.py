"""parent obj for resources"""

import jamfpy
from requests import HTTPError
from .hcl import generate_imports
from .exceptions import InvalidResourceTypeError, DataError, ImporterConfigError
from .constants import RESOURCE_TYPES, ILLEGAL_NAME_CHARS
from .options import Options, Applicator


class Resource:
    """parent obj for resources"""
    resource_type = ""

    def __init__(self, options: Options = None, validate: bool = True, client: jamfpy.JamfTenant = None, log_level: int = 20):
        if not self.resource_type:
            raise InvalidResourceTypeError(f"Instantiate a specific resource type and not the parent {self.resource_type}")

        self.data = {}
        self.options = options if options is not None else Options()
        self.applicator = Applicator(self.resource_type, opts=self.options.options(), validate=validate)
        self.client = client
        self.logger = jamfpy.get_logger(f"Resource - {self.resource_type}", log_level)
        

    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"


    # Private

    def _apply_options(self):
        """sends data through applicator object to have options applied"""        
        self.data = self.applicator.apply(self.data)
   

    def _get(self):
        self.logger.info(f"getting data for resource type: {self.resource_type}")
        """
        Retrieves data from api and should always populate self.data with:
        {
            "jamfpro_resourcename.id": {
                "id": X,
                "name": Y
            }
        }
        """

        if isinstance(self, Resource):
            raise ImporterConfigError("operation invalid at Resource level. Please define a resource type")


    # Public

    def set_client(self, client: jamfpy.JamfTenant, refresh_data: bool = False):
        """function to wrap setting of object bound client"""
        self.logger.info("setting client...")

        assert isinstance(client, jamfpy.JamfTenant), "invalid client type"
        self.client = client

        if refresh_data:
            self.refresh_data()


    def set_options(self, options: Options, apply: bool = False):
        """set_options allows options to be set after instantiation"""
        assert isinstance(options, Options)
        self.options = options

        if apply:
            self._apply_options()


    def refresh_data(self):
        """refreshes data held by object from api"""
        self.logger.info("refreshing cached data...")

        if self.client is None:
            raise ImporterConfigError("no client provided. Provide client via object creation or .set_client(client)")

        self._get()
        self._apply_options()


    def build_hcl(self):
        """Generates HCL for all Script attrs"""
        return generate_imports(self.resource_type, self.data)


class Scripts(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPES["script"]

    def _get(self):
        super()._get()
        """
        Retrieves data from api and should always populate self.data with:
        {
            "name.id": {
                "id": id,
                "name": name
            }
        }
        """

        resp, data = self.client.pro.scripts.get_all()
        if not resp.ok:
            raise HTTPError("bad api call")

        for i in data:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"],
            }


class Categories(Resource):
    """catagories"""
    resource_type = RESOURCE_TYPES["category"]

    def _get(self):
        super()._get()
        resp = self.client.classic.categories.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["categories"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"]
            }
