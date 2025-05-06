"""Main importer object."""

from typing import List
import jamfpy
from .exceptions import ImporterConfigError
from .models import Resource


class Importer:
    """
    Manages and imports targetted Jamf resources.

    Args:
        client (jamfpy.Tenant): Jamf API client.
        targetted (List[Resource]): Resources to manage and import.

    Raises:
        AssertionError: If client or target types are invalid.
        ImporterConfigError: If no resources are provided.
    """

    targetted: List[Resource]

    def __init__(self, client: jamfpy.Tenant, targetted: List[Resource]):

        if not targetted:
            raise ImporterConfigError("No resources provided")

        for resource in targetted:
            resource.set_client(client)
            resource.refresh_data()

        self.targetted = targetted


    def refresh(self):
        """Refresh all resource data."""
        for resource in self.targetted:
            resource.refresh_data()


    def hcl_s(self) -> str:
        """Return all import blocks as a single joined string."""

        return "\n".join(block for block in self.hcl_d().values())


    def hcl_d(self) -> dict:
        """Return import blocks grouped by resource type."""
        out = {}

        for resource in self.targetted:
            hcl = "\n".join(resource.build_hcl())
            out.setdefault(resource.resource_type, "")
            out[resource.resource_type] += f"\n{hcl}"

        return out
