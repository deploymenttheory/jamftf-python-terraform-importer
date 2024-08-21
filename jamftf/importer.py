
from .exceptions import jamftf_importer_config_error
from .resources import Resource
from typing import List
import jamfpy

class Importer:
    targetted: list[Resource] = None
    def __init__(self, client: jamfpy.JamfTenant, targetted: List[Resource]):

        if len(targetted) == 0:
            raise jamftf_importer_config_error("no targets set")

        for t in targetted:
            t.set_client(client)

        self.targetted = targetted


    def Refresh(self):
        for t in self.targetted:
            t.get()
            t.apply_options()


    def HCL(self):
        out = ""
        for r in self.targetted:
            out += "\n".join(r.hcl())

        return out
            
    

            


