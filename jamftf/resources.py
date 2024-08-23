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

    def __init__(self, options: Options = None, validate: bool = True, client: jamfpy.JamfTenant = None):
        if not self.resource_type:
            raise InvalidResourceTypeError(f"Instantiate a specific resource type and not the parent {self.resource_type}")

        self.data = {}
        opts_schema = options.options() or Options().options()
        self.applicator = Applicator(self.resource_type, opts=opts_schema, validate=validate)
        

        if client:
            self.client = client
            self.refresh_data()


    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"


    # Private

    def _apply_options(self):
        """sends data through applicator object to have options applied"""

        if not self.options:
            return
        
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

    def set_client(self, client: jamfpy.JamfTenant):
        """function to wrap setting of object bound client"""

        assert isinstance(client, jamfpy.JamfTenant), "invalid client type"
        self.client = client


    def refresh_data(self):
        """refreshes data held by object from api"""
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
        resp = self.client.classic.categories.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in resp.json()["categories"]:
            self.data[f"{i['name']}.{i['id']}"] = {
                "id": i["id"],
                "name": i["name"]
            }
