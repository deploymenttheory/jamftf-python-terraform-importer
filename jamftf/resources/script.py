"""script specific handling"""

from .constants import RESOURCE_TYPE_SCRIPT
from ..hcl import generate_imports
from .resource import Resource, ResourceOptions
from requests import HTTPError


class Script(Resource):
    """Script obj"""
    resource_type = RESOURCE_TYPE_SCRIPT
    data = []
    options: ResourceOptions

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

        self.data = out


