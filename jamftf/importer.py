from .resources.script import Script

class Importer:
    def __init__(self, client, use_jamf_name: bool):
        self.scripts = Script(client, use_jamf_name)


