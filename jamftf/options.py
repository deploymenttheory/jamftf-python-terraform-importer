"""home of options"""
from logging import Logger
from .constants import ILLEGAL_NAME_CHARS, REQUIRED_RESOURCE_CONFIG_KEYS, VALID_RESOURCE_CONFIG_KEYS
from .exceptions import DataError


class Options:
    """Options is a small framework for generating options schemas"""
    def __init__(
            self,
            use_resource_type_as_name = False,
        ):

        self.out = {}
        self.out["use_resource_type_as_name"] = use_resource_type_as_name


    def options(self):
        """returns options from self"""
        return self.out

    def add(self, key, value):
        """allows method bound addition of options"""
        if key not in VALID_RESOURCE_CONFIG_KEYS:
            raise DataError(f"attemped to add invalid config key: {key}")

        self.out[key] = value

    def from_json(self, data: dict):
        """generates options from dict"""
        self.out = data
        return self


class Applicator:
    """
    Applicator holds interfaced methods for applying options form json schema
    """
    def __init__(
            self,
            resource_type: str,
            opts: dict,
            validate: bool,
            logger: Logger,
            exclude_ids: list[int] = list
        ):

        self.opts = opts
        self.resource_type = resource_type
        self.validate = validate
        self.lg = logger
        self.exclude_ids = exclude_ids


    def apply(self, data: dict):
        """applies options to supplied data"""
        self.lg.info("applying options...")

        options_master = {
            "use_resource_type_as_name": self._use_resource_type_as_name
        }

        for o in self.opts:

            if o in REQUIRED_RESOURCE_CONFIG_KEYS:
                continue

            self.lg.debug(f"handling {o}...")

            if self.opts[o]:
                self.lg.debug(f"{o} flagged to be set")

                data = options_master[o](data)

                self.lg.info(f"{o} set for {self.resource_type}")


        if self.exclude_ids:
            data = self._exclude_ids(data)

        if self.validate:
            self._validation(data)

        return data


    def _validation(self, data):
        """_validation is a parent func for running data validation functions"""

        self.lg.debug("validating data...")

        self._check_illegal_chars(data)
        self._check_duplicates(data)


    def _exclude_ids(self, data: dict) -> dict:
        """removes any IDs from the data which have been specifid to be excluded"""

        to_delete = []
        for i in data:

            res_id = int(data[i]["id"])

            if res_id in self.exclude_ids:

                self.lg.debug(f"{res_id} marked for deletion")

                to_delete.append(i)


        self.lg.debug("deleting excluded records")
        for i in to_delete:
            del data[i]

        return data


    def _use_resource_type_as_name(self, data: dict) -> dict:
        """change the names of all resources held in data to resource_name.XX"""
        self.lg.debug("amending resource names...")

        counter = 0
        for i in data:
            data[i]["name"] = f"{self.resource_type}_{counter}"
            counter += 1

        return data


    def _check_illegal_chars(self, data: dict):
        """sweeps resource names for chars invalid in HCL"""
        self.lg.debug(f"checking for illegal chars: {ILLEGAL_NAME_CHARS}")

        for i, j in data.items():
            for c in data[i]["name"]:
                if c in ILLEGAL_NAME_CHARS:
                    raise DataError(f"Illegal char: '{c}' found in {self.resource_type}, id: {j["id"]}, name: {j['name']}")


    def _check_duplicates(self, data: dict):
        """iterates through all resource names ensuring no duplicates"""
        self.lg.debug("checking for duplicates")


        keys = {}
        for i in data:
            name = data[i]["name"]
            if name not in keys:
                keys[name] = 1
            elif name in keys:
                keys[name] += 1
            else:
                raise DataError("you shouldn't be here")

        duplicates = []
        for i, j in keys.items():
            if j > 1:
                duplicates.append(i)

        if duplicates:
            nl = "\n"
            raise DataError(f"Duplcate named resources found: {nl.join(duplicates)}")
