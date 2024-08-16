from .resources.script import Script

class Importer:
    def __init__(self, client, targetted: list):
        self._client = client
        self._targetted = targetted

    def HCL(self):
        hcl = ""
        for res in self._targetted:
            for i in res.HCL():
                hcl += i

        return hcl

            


