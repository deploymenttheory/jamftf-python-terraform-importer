"""script specific handling"""

from .constants import RESOURCE_TYPE_SCRIPT
from ..hcl import generate_imports
from .resource import Resource
from requests import HTTPError


class Script(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPE_SCRIPT

    # Priv
    def _get(self, exclude: list = []):
        """
        must always return
        [
            {
                "id": ID
                "name": NAME
            },
            ...
            ...
        ]
        """
        out = []
        resp, data = self.client.pro.scripts.get_all()

        if not resp.ok:
            raise HTTPError("bad api call")

        count = 0
        for i in data:
            if i["id"] not in exclude:
                out.append({
                    "id": i["id"],
                    "name": i["name"]
                })

                count += 1

        return out


    # Public
    def HCL(self):
        """Generates HCL for all Script attrs"""
        return generate_imports({
            "resource_type": self.resource_type,
            "resources": self._get()
        })
