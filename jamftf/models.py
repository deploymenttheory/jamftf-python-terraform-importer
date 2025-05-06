from logging import Logger
import jamfpy
import abc
from .exceptions import InvalidResourceTypeError, ImporterConfigError
from .hcl import generate_imports

LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20

class SingleItem:
    def __init__(self, resource_type, jpro_id):
        self.resource_type = resource_type
        self.jpro_id = jpro_id


class Resource:
    """parent obj for resources"""
    resource_type = ""
    lg: Logger

    def __init__(
            self,
            client: jamfpy.Tenant = None,
            debug: bool = False,
        ):

        log_level = LOG_LEVEL_DEBUG if debug else LOG_LEVEL_INFO

        self._init_logger(log_level)

        # TODO why do we do this?
        self.data = []

        self.client = client

        self.lg.info("resource initilized: %s", self.resource_type)


    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"


    def _init_logger(self, log_level: int):
        """_init_logger initilizes a logger"""
        self.lg = jamfpy.get_logger(f"resource-{self.resource_type}", level=log_level)


    def _log_get(self):
        """standardises log for getting data"""
        self.lg.info("getting data for resource type: %s", self.resource_type)


    @abc.abstractmethod
    def _get(self):
        """
        Retrieves data from api and should always populate self.data with:
        {
            "jamfpro_resourcename.id": {
                "id": X,
                "name": Y
            }
        }
        """
        pass


    # Public

    def build_hcl(self):
        """Generates HCL for all Script attrs"""
        return generate_imports(self.resource_type, self.data)


    def set_client(self, c: jamfpy.Tenant):
        self.client = c


    def refresh_data(self):
        """refreshes data held by object from api"""
        self.lg.info("refreshing data...")

        if self.client is None:
            raise ImporterConfigError("no client provided. Provide client via object creation or .set_client(client)")

        self._get()




