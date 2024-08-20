
from .exceptions import jamftf_importer_config_error
from .resources import Resource
from typing import List
import jamfpy

class Importer:
    hcl = ""
    targetted: list[Resource] = None
    def __init__(self, client: jamfpy.JamfTenant, targetted: List[Resource]):

        if len(targetted) == 0:
            raise jamftf_importer_config_error("no targets set")

        self.targetted = targetted

        for t in self.targetted:
            t.set_client(client)
            t.get()
            t.apply_options()


    def Get(self):
        for t in self.targetted:
            t.get()
            t.apply_options()
            self.hcl += "\n".join(t.hcl())

    def HCL(self):
        hcl = ""
        for resource in self.targetted:
            hcl += "\n".join(resource.hcl())
        
        self.hcl = hcl
        return self.hcl
    

            


