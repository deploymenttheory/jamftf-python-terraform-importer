"""Main importer object."""

from typing import List, Set
import jamfpy
from .exceptions import ConfigError, ImporterError
from .models import Resource

class Importer:
    """
    Manages and imports targetted Jamf resources.

    Args:
        client (jamfpy.Tenant): Jamf API client.
        targetted (List[Resource]): Resources to manage and import.

    Raises:
        AssertionError: If client or target types are invalid.
        ConfigError: If no resources are provided.
    """

    targetted: List[Resource]

    def __init__(self, client: jamfpy.Tenant, targetted: List[Resource]):
        if not targetted:
            raise ConfigError("No resources provided")

        for resource in targetted:
            resource.set_client(client)

        self.targetted = targetted
        self.refresh()

    def refresh(self):
        """Refresh all resource data."""
        for resource in self.targetted:
            resource.refresh_data()

    def hcl_s(self) -> str:
        """Return all import blocks as a single joined string."""
        blocks = set()  # Use a set to deduplicate
        for resource_type, hcl in self.hcl_d().items():
            if hcl:  # Only add if there's content
                blocks.add(hcl)
        return "\n".join(sorted(blocks))  # Sort for consistent output

    def hcl_d(self) -> dict:
        """Return import blocks grouped by resource type."""
        out = {}

        for resource in self.targetted:
            hcl = resource.build_hcl()
            if hcl:  # Only add if there's content
                out[resource.resource_type] = hcl

        return out
