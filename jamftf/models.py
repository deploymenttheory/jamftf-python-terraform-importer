"""Base class for Jamf resource types."""

import abc
from logging import Logger
from typing import Callable, Optional, Any
from requests import Response
import jamfpy
from .exceptions import ConfigError
from .hcl import generate_imports
from .dataclasses import SingleItem

LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20

class Resource:
    """Parent object for Jamf Pro resources."""
    resource_type = ""
    lg: Logger

    def __init__(self, client: jamfpy.Tenant = None, debug: bool = False):
        log_level = LOG_LEVEL_DEBUG if debug else LOG_LEVEL_INFO
        self._init_logger(log_level)
        self.data = []
        self.client = client
        self.lg.info("resource initialized: %s", self.resource_type)

    def __str__(self):
        return f"Jamf Pro Resource of type: {self.resource_type}"

    def _init_logger(self, log_level: int):
        """Initialises a logger for the resource."""
        self.lg = jamfpy.get_logger(f"resource-{self.resource_type}", level=log_level)

    def _log_get(self):
        """Logs a standard message for data fetch operations."""
        self.lg.info("getting data for resource type: %s", self.resource_type)

    @abc.abstractmethod
    def _get(self):
        """Fetch data and populate self.data (to be implemented by subclasses)."""

    def _get_from_api(
        self,
        api_call: Callable[[], Response],
        response_key: str,
        id_field: str = "id",
        filter_fn: Optional[Callable[[dict], bool]] = None,
    ) -> None:
        """
        Fetch and store resource data as SingleItem objects.

        Args:
            api_call: No-arg function that returns a requests.Response.
            response_key: Top-level key in the response JSON to iterate.
            id_field: Field in each item to extract as the unique ID (default: "id").
            filter_fn: Optional function to filter items by content.

        Raises:
            ConfigError: If the response key is not found in the API response.
        """
        self._log_get()
        resp = api_call()
        resp.raise_for_status()
        
        # Debug the response structure
        response_data = resp.json()
        self.lg.info("API Response: %s", response_data)
        
        # Check if response_key is in the response
        if response_key not in response_data:
            available_keys = list(response_data.keys())
            error_msg = f"Response key '{response_key}' not found in API response. Available keys: {available_keys}"
            self.lg.error(error_msg)
            raise ConfigError(error_msg)

        # Debug first item
        if response_data[response_key]:
            first_item = response_data[response_key][0]
            self.lg.info("First item data: %s", first_item)
            self.lg.info("Available fields: %s", list(first_item.keys()))

        for item in response_data[response_key]:
            if filter_fn and not filter_fn(item):
                continue
            self.data.append(SingleItem(self.resource_type, item["name"], item[id_field]))

    def build_hcl(self):
        """Generate HCL for all resource data."""
        return generate_imports(self.data)

    def set_client(self, client: jamfpy.Tenant):
        """Assign a Jamf client to the resource."""
        self.client = client

    def refresh_data(self):
        """Refresh data held by the object from the API."""
        self.lg.info("refreshing data...")
        if self.client is None:
            raise ConfigError("no client provided. Provide client via object creation or .set_client(client)")
        self._get()
