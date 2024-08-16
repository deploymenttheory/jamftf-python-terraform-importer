"""parent obj for resources"""

import jamfpy
from ..hcl import generate_imports
from ..exceptions import jamftf_importer_config_error
from .constants import *
from requests import HTTPError

class Options:
    """options container, to be expanded"""
    use_jamf_name: bool = False
    exclude_ids: list = []

    def __init__(self, use_jamf_name = False, exclude_ids = []):
        self.use_jamf_name = use_jamf_name
        self.exclude_ids = exclude_ids


class Resource:
    """parent obj for resources"""
    resource_type = ""
    client = None
    _data = []
    _options: Options

    def __init__(
            self,
            options = None
            ):
        
        if options == None:
            self.options = Options()


    def _set_client(self, client: jamfpy.JamfTenant):
        self.client = client
    

    def generate_hcl(self):
        """Generates HCL for all Script attrs"""

        if not self.resource_type:
            raise jamftf_importer_config_error("no resource type set")
        
        return generate_imports({
            "resource_type": self.resource_type,
            "resources": self._get()
        })



class Script(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPE_SCRIPT

    # Priv
    def _get(self):
        """
        must always return
        [
            {
                "id": ID
                "name": NAME
            },
            ...
            ...
        ]
        """
        out = []
        resp, data = self.client.pro.scripts.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        for i in data:
            if i["id"] not in self.options.exclude_ids:
                out.append({
                    "id": i["id"],
                    "name": i["name"]
                })

        self._data = out
        return out


class Categories(Resource):
    resource_type = RESOURCE_TYPE_CATEGORIES

    def _get(self):
        out = []
        resp = self.client.classic.categories.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")
        
        for i in resp.json():
            if i["id"] not in self.options.exclude_ids:
                out.append({
                    "id": i["id"],
                    "name": i["name"]
                })

        self._data = out
        return out

    
            


