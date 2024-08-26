"""home of options"""
from .constants import ILLEGAL_NAME_CHARS
from .exceptions import DataError

class Options:
    """Options is a small framework for generating options schemas"""
    def __init__(
            self,
            use_resource_type_as_name = False,
            exclude_ids: dict = None,
        ):
        
        self.out = {}
        self.out["use_resource_type_as_name"] = use_resource_type_as_name
        self.out["exclude_ids"] = exclude_ids or {}

    
    def options(self):
        return self.out
    
    def add(self, key, value):
        self.out[key] = value

    def from_json(self, data: dict):
        self.out = data

        

class Applicator:
    """
    Applicator holds interfaced methods for applying options form json schema
    """
    def __init__(self, resource_type, opts, validate):
        self.opts = opts
        self.resource_type = resource_type
        self.validate = validate


    def apply(self, data: dict):
        OPTIONS_MASTER = {
            "exclude_ids": self.exclude_ids,
            "use_resource_type_as_name": self._use_resource_type_as_name,
        }

        for o in self.opts:
            if self.opts[o]:
                data = OPTIONS_MASTER[o](data)


        if self.validate:
            self._validation(data)

        return data
    

    def _validation(self, data):
        self._check_illegal_chars(data)
        self._check_duplicates(data)


    def exclude_ids(self, data: dict) -> dict:
        """removes any IDs from the data which have been specifid to be excluded"""
        
        if self.resource_type not in self.opts["exclude_ids"]:
            # warn
            return data

        to_delete = []
        for i in data:
            if int(data[i]["id"]) in self.opts["exclude_ids"][self.resource_type]:
                to_delete.append(i)

        for i in to_delete:
            del data[i]

        return data


    def _use_resource_type_as_name(self, data: dict) -> dict:
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
                    raise DataError(f"Illegal char: '{c}' found in res: {i}, name: {data[i]["name"]}")


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




