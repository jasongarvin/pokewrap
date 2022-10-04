"""
The beginnings of a module designed to wrap the PokeAPI API and consume
it easier in Python and within the Pokemon Tools library.
"""

import json
import requests


API_URI_STUB = "https://pokeapi.co/api/v2/"


class apiController:
    """An object that manages the connection between pokeapi
    (https://pokeapi.co/) and the running application."""

    def __init__(self, api_address, cache_path="cache.json"):
        """Initializes the apiController with default uri
        to enable HTTP requests to the API source."""
        self.cache_path = cache_path
        self.address = api_address
        self.resources = None

    def cache_resource(self):
        """Save the received resources from API call to JSON file"""
        with open(self.cache_path, "r+", encoding="utf-8") as file:
            file_data = json.load(file)

            file_data[self.address] = self.resources[self.address]

            file.seek(0)
            json.dump(file_data, file)

    def get_resource(self):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it.

        Returns a dictionary of JSON-formatted data."""
        try:
            response = requests.get(self.address, timeout=10)
            response.raise_for_status()
            print(response)
            self.resources = {self.address: response.json()}

            return self.resources
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return {}

    def set_address(self, address):
        """Change the stored address."""
        self.address = address
