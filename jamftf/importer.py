"""main importer object"""
from typing import List
import jamfpy
from .exceptions import ImporterConfigError, OptionsConflictError
from .resources import Resource

class Importer:
    """object for managing all targetted resources"""

    targetted: list[Resource] = None
    def __init__(self, client: jamfpy.JamfTenant, targetted: List[Resource]):

        assert isinstance(client, jamfpy.JamfTenant), "incorrect client type"

        if len(targetted) == 0:
            raise ImporterConfigError("no targets set")

        for t in targetted:
            t.set_client(client)
            t.refresh_data()

        self.targetted = targetted


    def Refresh(self):
        """refreshes data held by resource objects"""
        for t in self.targetted:
            t.refresh_data()


    def HCL(self):
        """generates hcl on every targetted object"""
        out = ""
        for r in self.targetted:
            out += "\n" + "\n".join(r.build_hcl()) + "\n"

        return out
