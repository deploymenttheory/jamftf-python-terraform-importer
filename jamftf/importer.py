"""main importer object"""
from typing import List
import jamfpy
from .exceptions import ImporterConfigError
from .models import Resource

class Importer:
    """
    A class for managing and importing targetted resources from a Jamf tenant.

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
        Refresh(): Refreshes the data for all targetted resources.
        HCL(): Generates HCL (HashiCorp Configuration Language) for all targetted resources.
    """

    targetted: list[Resource]
    def __init__(
            self,
            client: jamfpy.Tenant,
            targetted: List[Resource],
        ):

        assert isinstance(client, jamfpy.Tenant), f"invalid client type {type(client)}"

        if not targetted:
            raise ImporterConfigError("no targets set")

        assert all(isinstance(t, Resource) for t in targetted), "invalid resource type provided"

        for t in targetted:
            t.set_client(client)
            t.refresh_data()

        self.targetted = targetted


    def refresh(self):
        """refreshes data held by resource objects"""
        for t in self.targetted:
            t.refresh_data()


    def hcl_s(self):
        """
        Generates HCL as a dict
        Joins it into stringd 
        """
        out = ""
        hcld = self.hcl_d()
        for i in hcld.values():
            out += (i + "\n")

        return out


    def hcl_d(self):
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
