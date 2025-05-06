"""Storage for dataclases"""

from dataclasses import dataclass

@dataclass
class SingleItem:
    """Represents a single Jamf resource item."""
    def __init__(self, resource_type, jpro_id):
        self.resource_type = resource_type
        self.jpro_id = jpro_id
