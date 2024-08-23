"""main importer object"""
from typing import List
import jamfpy
from .exceptions import ImporterConfigError, OptionsConflictError
from .resources import Resource
from .options import Options

class Importer:
    """object for managing all targetted resources"""

    targetted: list[Resource] = None
    def __init__(self, client: jamfpy.JamfTenant, targetted: List[Resource], global_options: Options = None):

        assert isinstance(client, jamfpy.JamfTenant), "incorrect client type"

        if len(targetted) == 0:
            raise ImporterConfigError("no targets set")

        for t in targetted:
            if global_options is not None:
                global_options_dict = global_options.options()
                for k in global_options_dict:
                    if k in t.options.options():
                        raise OptionsConflictError(f"conflicting option: {k}")
                    
                    t.options.add(k, global_options_dict[k])


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
            out += "\n".join(r.build_hcl()) + "\n"

        return out
