"""parent obj for resources"""

import jamfpy
from ..hcl import generate_imports
from ..exceptions import jamftf_importer_config_error

class ResourceOptions:
    use_jamf_name: bool = False
    exclude_ids: list = []

    def __init__(self, use_jamf_name = False, exclude_ids = None):
        self.use_jamf_name = use_jamf_name
        self.exclude_ids = exclude_ids


class Resource:
    """parent obj for resources"""
    resource_type = ""
    client = None

    def __init__(
            self,
            options: ResourceOptions
            ):
        
        self.options = options


    def _set_client(self, client: jamfpy.JamfTenant):
        self.client = client
    

    def HCL(self):
        """Generates HCL for all Script attrs"""

        if not self.resource_type:
            raise jamftf_importer_config_error("no resource type set")
        
        return generate_imports({
            "resource_type": self.resource_type,
            "resources": self._get()
        })
