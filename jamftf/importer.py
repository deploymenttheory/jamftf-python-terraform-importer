
from .exceptions import jamftf_importer_config_error
from .resources import Resource
from typing import List
import jamfpy

class Importer:
    def __init__(self, client: jamfpy.JamfTenant, targetted: List[Resource]):

        if len(targetted) == 0:
            raise jamftf_importer_config_error("no targets set")

        self._targetted = targetted

        for t in self._targetted:
            t.set_client(client)
            t.get()
            t.apply_options()


    def HCL(self):
        hcl = ""
        for resource in self._targetted:
            hcl += "\n".join(resource.hcl())

        self.hcl = hcl
        return hcl
    

            


