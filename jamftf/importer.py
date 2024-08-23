"""main importer object"""
from typing import List
import jamfpy
from .exceptions import ImporterConfigError, OptionsConflictError
from .resources import Resource
from .options import Options
from random import randint
import os

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


    def HCL(self, pretty: bool = True, cwd: str = ""):
        """generates hcl on every targetted object"""
        out = ""
        for r in self.targetted:
            out += "\n" + "\n".join(r.build_hcl()) + "\n"

        pretty_hcl = ""
        fp = f"{cwd}/temp_{randint(1, 9999)}.tf"
        if pretty:
            if not cwd:
                raise ImporterConfigError("no working dir given")
            with open(fp, "w") as f:
                f.write(out)

            os.system("terraform fmt")

            with open(fp, "r") as f:
                pretty_hcl = f.read()

            # os.remove(fn)

            out = pretty_hcl

        return out
