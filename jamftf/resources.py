"""parent obj for resources"""

import jamfpy
from requests import HTTPError
from .hcl import generate_imports
from .exceptions import InvalidResourceTypeError, ImporterConfigError
from .constants import RESOURCE_TYPES
from .options import Options, Applicator


class Resource:
    """parent obj for resources"""
    resource_type = ""

    def __init__(
            self, 
            options: Options = None, 
            validate: bool = True, 
            client: jamfpy.JamfTenant = None, 
            debug: bool = False
        ):

        self._validate_resource_type()

        log_level = self._init_log_level(debug)
        self._init_logger(log_level)

        self._init_applicator(log_level, validate)

        self.data = {}
        self.options = options if options is not None else Options()
        self.client = client

        self.lg.info(f"resource initilized: {self.resource_type}")


    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"


    # Private

    def _init_applicator(self, log_level, validate):
        """init_applicator initilizes an applicator and adds a logger"""
        logger = jamfpy.get_logger(f"applicator({self.resource_type})", level=log_level)
        self.applicator = Applicator(self.resource_type, opts=self.options.options(), validate=validate, logger=logger)


    def _init_logger(self, log_level: int):
        """_init_logger initilizes a logger"""
        self.lg = jamfpy.get_logger(f"Resource - {self.resource_type}", log_level)


    def _init_log_level(self, debug: bool) -> int:
        """init logging implements a simple two level logging approach"""
        assert isinstance(debug, bool), "debug flag is not bool"

        log_levels = {
            True: 10,
            False: 20,
        }

        return log_levels[debug]


    def _validate_resource_type(self):
        """_validate_resource_type validates that the resource type parameter is set"""
        if not self.resource_type:
            raise InvalidResourceTypeError(f"Instantiate a specific resource type and not the parent {self.resource_type}")


    def _apply_options(self):
        """sends data through applicator object to have options applied""" 
        self.lg.debug("applying options...")       
        self.data = self.applicator.apply(self.data)

    
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

    def set_client(self, client: jamfpy.JamfTenant, refresh_data: bool = False):
        """function to wrap setting of object bound client"""
        self.lg.debug("setting client...")

        assert isinstance(client, jamfpy.JamfTenant), "invalid client type"
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
            self._apply_options()


    def refresh_data(self):
        """refreshes data held by object from api"""
        self.lg.info("refreshing data...")

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
        self.lg.info(f"getting data for resource type: {self.resource_type}")
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
        self.lg.info(f"getting data for resource type: {self.resource_type}")

        resp = self.client.classic.categories.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["categories"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"]
            }
