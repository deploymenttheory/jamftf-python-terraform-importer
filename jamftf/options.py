"""home of options"""
from .constants import ILLEGAL_NAME_CHARS
from .exceptions import DataError

class Options:
    """Options is a small framework for generating options schemas"""
    def __init__(
            self,
            use_resource_type_as_name = False,
            exclude_ids: list = None,
            ignore_illegal_chars = False,
            enable_validation = True
        ):

        self.use_resource_type_as_name = use_resource_type_as_name
        self.exclude_ids = exclude_ids or []
        self.ignore_illegal_chars = ignore_illegal_chars
        self.enable_validation = enable_validation


    def _generate_output(self):
        """generates output"""
        return {
            "use_resource_type_as_name": self.use_resource_type_as_name,
            "exclude_ids": self.exclude_ids,
            "ignore_illegal_chars": self.ignore_illegal_chars,
            "enable_validation": self.enable_validation
        }
    
    def options(self):
        return self._generate_output()


class Applicator:
    """
    Applicator holds interfaced methods for applying options form json schema
    """
    def __init__(self, resource_type):
        self.resource_type = resource_type


    def apply(self, data: dict, opts: dict):
        self.opts = opts
        OPTIONS_MASTER = {
            "exclude_ids": self.exclude_ids,
            "use_resource_type_as_name": self.use_resource_type_as_name,
            "enable_validation": self._validation
        }

        for o in opts:
            if opts[o]:
                OPTIONS_MASTER[o](data)

        return data

    def _validation(self, data):
        self._check_illegal_chars(data)
        self._check_duplicates(data)


    def exclude_ids(self, data: dict) -> dict:
        """removes any IDs from the data which have been specifid to be excluded"""
        to_delete = []
        for i in data:
            if int(data[i]["id"]) in self.opts["exclude_ids"]:
                to_delete.append(data[i])

        for i in to_delete:
            del data[i]

        return data


    def use_resource_type_as_name(self, data: dict) -> dict:
        """change the names of all resources held in data to resource_name.XX"""

        counter = 0
        for i in data:
            data[i]["name"] = f"{self.resource_type}.{counter}"
            counter += 1

        return data
        

    def _check_illegal_chars(self, data: dict):
        """sweeps resource names for chars invalid in HCL"""
        for i in data:
            for c in data[i]["name"]:
                if c in ILLEGAL_NAME_CHARS:
                    raise DataError(f"Illegal char: {c} found in res: {i}, name: {data[i]["name"]}")


    def _check_duplicates(self, data: dict):
        """iterates through all resource names ensuring no duplicates"""
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
        for i in keys:
            if keys[i] > 1:
                duplicates.append(i)

        if duplicates:
            raise DataError(f"Duplcate named resources found: {'\n'.join(duplicates)}")




