"""
The beginnings of a module designed to wrap the PokeAPI API and consume
it easier in Python and within the Pokemon Tools library.
"""

import requests


API_URI_STUB = "https://pokeapi.co/api/v2/"


class apiController:
    """An object that manages the connection between pokeapi
    (https://pokeapi.co/) and the running application."""

    def __init__(self, address=API_URI_STUB):
        """Initializes the apiController with default uri
        to enable HTTP requests to the API source."""
        self.address = address
        self.resource = None

    def get_resource(self, resource_type, resource_name):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it."""
        resource_uri = "/".join((self.address, resource_type, resource_name))
        resource = requests.get(resource_uri, timeout=10)

        self.resource = resource
        return resource
