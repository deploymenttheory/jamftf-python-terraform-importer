from logging import Logger
import jamfpy
import abc
from .options import Options, Applicator
from .exceptions import InvalidResourceTypeError, ImporterConfigError
from .hcl import generate_imports

LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20


class Resource:
    """parent obj for resources"""
    resource_type = ""
    lg: Logger

    def __init__(
            self,
            options: Options = None,
            validate: bool = True,
            client: jamfpy.Tenant = None,
            debug: bool = False,
            exclude: list[int] = None
        ):


        # TODO this can be turned into an abstract method?
        # self._validate_resource_type()

        log_level = LOG_LEVEL_DEBUG if debug else LOG_LEVEL_INFO

        self._init_logger(log_level)

        # TODO why do we do this?
        self.data = {}

        # Attrs setting
        self.client = client
        self.exclude = exclude

        # Why do we do this?
        self.options = options if options is not None else Options()

        # Do we need this? Options can probably be set at a later date.
        # Does it need it's own log level? 
        # self._init_applicator(log_level, validate)

        self.lg.info("resource initilized: %s", self.resource_type)


    # Magic

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"


    # Private

    # def _init_applicator(self, log_level, validate):
    #     """init_applicator initilizes an applicator and adds a logger"""
    #     logger = jamfpy.get_logger(f"applicator({self.resource_type})", level=log_level)
    #     self.applicator = Applicator(
    #         self.resource_type,
    #         opts=self.options.options(),
    #         validate=validate,
    #         logger=logger,
    #         exclude_ids=self.exclude
    #     )


    def _init_logger(self, log_level: int):
        """_init_logger initilizes a logger"""
        self.lg = jamfpy.get_logger(f"resource-{self.resource_type}", level=log_level)


    # def apply_options(self):
    #     """sends data through applicator object to have options applied""" 
    #     self.lg.debug("applying options...")
    #     self.data = self.applicator.apply(self.data)


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

    # def set_options(self, options: Options, apply: bool = True):
    #     """set_options allows options to be set after instantiation"""
    #     self.lg.debug("setting options...")

    #     assert isinstance(options, Options)
    #     self.lg.debug("options type is correct")


    #     self.options = options
    #     self.lg.debug("options set successfully")

    #     if apply:
    #         self.apply_options()


    def set_client(self, c: jamfpy.Tenant):
        self.client = c


    def refresh_data(self):
        """refreshes data held by object from api"""
        self.lg.info("refreshing data...")

        if self.client is None:
            raise ImporterConfigError("no client provided. Provide client via object creation or .set_client(client)")

        self._get()


    def _use_resource_type_as_name(self) -> dict:
        """change the names of all resources held in data to resource_name.XX"""
        self.lg.info("amending resource names...")

        counter = 0
        for i in self.data:
            self.data[i]["name"] = f"{self.resource_type}_{counter}"
            counter += 1




