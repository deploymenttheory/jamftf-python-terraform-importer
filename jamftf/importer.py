"""main importer object"""
from typing import List
import jamfpy
from .exceptions import ImporterConfigError
from .resources import Resource
from logging import Logger

class Importer:
    """
    A class for managing and importing targeted resources from a Jamf tenant.

    This class handles the initialization, refreshing, and HCL generation for a collection
    of Resource objects associated with a Jamf tenant.

    Attributes:
        targetted (List[Resource]): A list of Resource objects to be managed.

    Args:
        client (jamfpy.JamfTenant): The Jamf tenant client used for API interactions.
        targetted (List[Resource]): A list of Resource objects to be managed.

    Raises:
        AssertionError: If the provided client is not an instance of jamfpy.JamfTenant.
        ImporterConfigError: If the targetted list is empty.

    Methods:
        Refresh(): Refreshes the data for all targeted resources.
        HCL(): Generates HCL (HashiCorp Configuration Language) for all targeted resources.
    """

    targetted: list[Resource] = None
    def __init__(
            self, 
            client: jamfpy.JamfTenant, 
            targetted: List[Resource], 
            logger: Logger = None,
            debug: bool = False
        ):

        self.logger = logger or jamfpy.get_logger(name="Importer", level=log_level)

        assert isinstance(client, jamfpy.JamfTenant), "incorrect client type"

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


    def HCL(self):
        """generates hcl on every targetted object"""
        out = ""
        for r in self.targetted:
            out += "\n" + "\n".join(r.build_hcl()) + "\n"

        return out
