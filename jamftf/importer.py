from .resources.script import Script

class Importer:
    targetted = []
    def __init__(self, client, use_jamf_name: bool):
        self.scripts = Script(client, use_jamf_name)
        self.targetted = [Script(client, use_jamf_name)]



    def HCL(self):
        hcl = ""
        for res in self.targetted:
            for i in res.HCL():
                hcl += i

        return hcl

            


