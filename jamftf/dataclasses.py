"""Storage for dataclasses."""

from dataclasses import dataclass

@dataclass
class SingleItem:
    """Represents a single Jamf resource item."""
    def __init__(self, resource_type, resource_name, jpro_id):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.jpro_id = jpro_id
