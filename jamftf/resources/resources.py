"""parent obj for resources"""

import jamfpy
from ..hcl import generate_imports
from ..exceptions import jamftf_importer_config_error, jamftf_data_error
from .constants import *
from requests import HTTPError

class Options:
    """options container, to be expanded"""
    def __init__(
            self, 
            use_resource_type_as_name = False, 
            exclude_ids = [],
            ignore_illegal_chars = False
        ):
        self.use_resource_type_as_name = use_resource_type_as_name
        self.exclude_ids = exclude_ids
        self.ignore_illegal_chars = ignore_illegal_chars

        if exclude_ids == None:
            exclude_ids = []


class Resource:
    """parent obj for resources"""
    resource_type = ""
    _data = {}
    client: jamfpy.JamfTenant = None

    def __init__(
            self,
            options: Options
            ):
        

        # validation
        if not self.resource_type:
            raise jamftf_importer_config_error(f"invalid resource type: {self.resource_type}")
        
        self.options = options



    def set_client(self, client: jamfpy.JamfTenant):
        """function to wrap setting of object bound client"""
        assert type(client) == jamfpy.JamfTenant, "invalid client type"
        self.client = client


    def get(self):
        """
        Retrieves data from api and should always populate self._data with:
        {
            "id": X,
            "name": Y
        }
        """

        raise jamftf_importer_config_error("operation invalid at Resource level. Please define a resource type")
    

    def apply_options(self):
        """application of options object"""

        # Remove duplicates
        if len(self.options.exclude_ids) > 0:
            for i in self._data:
                if self._data[i]["id"] in self.options.exclude_ids:
                    del self._data[i]

        # Name change
        if self.options.use_resource_type_as_name:
            count = 0
            for i in self._data:
                self._data[i]["name"] == f"{self.resource_type}-{count}"
                count += 1
            


    def hcl(self):
        """Generates HCL for all Script attrs"""
        
        return generate_imports({
            "resource_type": self.resource_type,
            "resources": self._data
        })



class Script(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPE_SCRIPT

    def get(self):
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
            self._data[f"{i["name"]}.{i["id"]}"] = i



# class Categories(Resource):
#     resource_type = RESOURCE_TYPE_CATEGORIES

#     def _get(self):
#         out = []
#         resp = self.client.classic.categories.get_all()

#         if not resp.ok:
#             raise HTTPError("bad api call")
        
#         for i in resp.json():
#             if i["id"] not in self.options.exclude_ids:
#                 out.append({
#                     "id": i["id"],
#                     "name": i["name"]
#                 })

#         self._data = out
#         return out

    
            


