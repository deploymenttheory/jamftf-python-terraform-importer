
from .exceptions import jamftf_importer_config_error

class Importer:
    def __init__(self, client, targetted: list):
        self._client = client

        if len(targetted) == 0:
            raise jamftf_importer_config_error("no targets set")
        
        self._targetted = targetted

        for t in self._targetted:
            t._set_client(self._client)

    def HCL(self):
        hcl = ""
        for resource in self._targetted:
            hcl += "\n".join(resource.generate_hcl())

        self.hcl = hcl
        return hcl
    

            


