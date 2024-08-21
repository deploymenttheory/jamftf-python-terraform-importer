
from .exceptions import importer_config_error
from .resources import Resource
from typing import List
import jamfpy

class Importer:
    targetted: list[Resource] = None
    def __init__(self, client: jamfpy.JamfTenant, targetted: List[Resource]):

        assert type(client) == jamfpy.JamfTenant, "incorrect client type"
        if len(targetted) == 0: raise importer_config_error("no targets set")

        for t in targetted:
            t.set_client(client)

        self.targetted = targetted


    def Refresh(self):
        """refreshes data held by resource objects"""
        for t in self.targetted:
            t.refresh_data()


    def HCL(self):
        """generates hcl on every targetted object"""
        out = ""
        for r in self.targetted:
            out += "\n".join(r.build_hcl()) + "\n"

        return out
            
    

            


