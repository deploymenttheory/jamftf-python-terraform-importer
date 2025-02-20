"""main importer object"""
from typing import List
import jamfpy
from .exceptions import ImporterConfigError
from .resources import Resource

class Importer:
    """
    A class for managing and importing targeted resources from a Jamf tenant.

    This class handles the initialization, refreshing, and HCL generation for a collection
    of Resource objects associated with a Jamf tenant.

    Attributes:
        targetted (List[Resource]): A list of Resource objects to be managed.

    Args:
        client (jamfpy.Tenant): The Jamf tenant client used for API interactions.
        targetted (List[Resource]): A list of Resource objects to be managed.

    Raises:
        AssertionError: If the provided client is not an instance of jamfpy.Tenant.
        ImporterConfigError: If the targetted list is empty.

    Methods:
        Refresh(): Refreshes the data for all targeted resources.
        HCL(): Generates HCL (HashiCorp Configuration Language) for all targeted resources.
    """

    targetted: list[Resource] = None
    def __init__(
            self,
            client: jamfpy.Tenant,
            targetted: List[Resource],
            debug: bool = False
        ):

        assert isinstance(client, jamfpy.Tenant), "incorrect client type"

        if len(targetted) == 0:
            raise ImporterConfigError("no targets set")

        for t in targetted:
            t.set_debug(debug)
            t.set_client(client)
            t.refresh_data()

        self.targetted = targetted


    def Refresh(self):
        """refreshes data held by resource objects"""
        for t in self.targetted:
            t.refresh_data()


    def HCLs(self):
        """
        Generates HCL as a dict
        Joins it into stringd
        """
        out = ""
        hcld = self.HCLd()
        for i in hcld.values():
            out += i + "\n"

        return out


    def HCLd(self):
        """
        Returns dict as:
        "resource_type: "import statements"
        """
        out = {}
        for r in self.targetted:
            if r.resource_type not in out:
                out[r.resource_type] = ""

            out[r.resource_type] += "\n" + "\n".join(r.build_hcl())


        return out
