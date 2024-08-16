"""parent obj for resources"""

import jamfpy

class Resource:
    """parent obj for resources"""
    def __init__(
            self, 
            client: jamfpy.JamfTenant, 
            use_jamf_name: bool = False,
            exclude_ids: list = []
            ):
        
        self.client = client

        self._use_jamf_name = use_jamf_name
        self._exclude_ids = exclude_ids