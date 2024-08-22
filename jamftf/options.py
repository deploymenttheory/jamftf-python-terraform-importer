"""home of options"""

class Options:
    """options container, to be expanded"""
    def __init__(
            self,
            use_resource_type_as_name = False,
            exclude_ids: list = None,
            ignore_illegal_chars = False,
            _from_json: dict = None
        ):

        if _from_json:
            self._parse_json_options(_from_json)
            return
        
        self.use_resource_type_as_name = use_resource_type_as_name
        self.exclude_ids = exclude_ids or []
        self.ignore_illegal_chars = ignore_illegal_chars
        

    def _parse_json_options(self, config: dict):
        """parses json"""
        self.use_resource_type_as_name = config["use_resource_type_as_name"]
        self.exclude_ids = config["exclude_ids"]
        self.ignore_illegal_chars = config["ignore_illegal_chars"]

        
