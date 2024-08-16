
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
        for res in self._targetted:
            for i in res.generate_hcl():
                hcl += i

        self.hcl = hcl
        return hcl
    

            


