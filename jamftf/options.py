"""home of options"""

class Options:
    """options container, to be expanded"""
    def __init__(
            self,
            use_resource_type_as_name = False,
            exclude_ids: list = None,
            ignore_illegal_chars = False
        ):

        self.use_resource_type_as_name = use_resource_type_as_name
        self.exclude_ids = exclude_ids or []
        self.ignore_illegal_chars = ignore_illegal_chars