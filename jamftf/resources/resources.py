"""parent obj for resources"""

import jamfpy
from ..hcl import generate_imports
from ..exceptions import importer_config_error, data_error
from .constants import *
from requests import HTTPError

class Options:
    """options container, to be expanded"""
    def __init__(
            self, 
            use_resource_type_as_name = False, 
            exclude_ids: list = [],
            ignore_illegal_chars = False
        ):
        self.use_resource_type_as_name = use_resource_type_as_name
        self.exclude_ids = exclude_ids
        self.ignore_illegal_chars = ignore_illegal_chars



class Resource:
    """parent obj for resources"""
    resource_type = ""
    client: jamfpy.JamfTenant = None

    def __init__(
            self,
            options: Options = None,
            client: jamfpy.JamfTenant = None
            ):


        # validation
        if not self.resource_type:
            raise importer_config_error(f"invalid resource type: {self.resource_type}")
        
        if client:
            self.client = client

        self._data = {}
        self.options = options

        self.refresh_data()


    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"
    

    # Private

    def _validation(self):
        """checks for illegal chars and more soon"""

        if self.options.ignore_illegal_chars:
            return
        
        for i in self._data:
            if any(c for c in ILLEGAL_NAME_CHARS in self._data[i]["name"]):
                raise data_error(f"illegal char found in {self.resource_type}: {self._data[i]}")


    def _options(self):
        """application of options object"""

        if self.options == None:
            return
        
        self._options_remove_duplicates()
        self._options_name_change()


    def _options_remove_duplicates(self):
        """removes dupes"""

        if len(self.options.exclude_ids) > 0:
            to_delete = []
            for i in self._data:
                if int(self._data[i]["id"]) in self.options.exclude_ids:
                    to_delete.append(i)

            for i in to_delete:
                del self._data[i]


    def _options_name_change(self):
        """changes name"""

        if self.options.use_resource_type_as_name:
            count = 0
            for i in self._data:
                self._data[i]["name"] = f"{self.resource_type}-{count}"
                count += 1


    def _get(self):
        """
        Retrieves data from api and should always populate self._data with:
        {
            "jamfpro_resourcename.id": {
                "id": X,
                "name": Y
            }
        }
        """

        raise importer_config_error("operation invalid at Resource level. Please define a resource type")


    # Public

    def set_client(self, client: jamfpy.JamfTenant):
        """function to wrap setting of object bound client"""
        assert type(client) == jamfpy.JamfTenant, "invalid client type"
        self.client = client


    def refresh_data(self):
        self._get()
        self._options()
        self._validation()


    def build_hcl(self):
        """Generates HCL for all Script attrs"""
        return generate_imports(self.resource_type, self._data)


class Scripts(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPE_SCRIPT

    def _get(self):
        """
        Retrieves data from api and should always populate self._data with:
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
            self._data[f"{i["name"]}.{i["id"]}"] = {
                "id": i["id"],
                "name": i["name"]
            }



class Categories(Resource):
    resource_type = RESOURCE_TYPE_CATEGORIES

    def _get(self):
        resp = self.client.classic.categories.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")
        
        for i in resp.json()["categories"]:
            self._data[f"{i["name"]}.{i["id"]}"] = {
                "id": i["id"],
                "name": i["name"]
            }



    
            


