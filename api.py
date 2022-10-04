"""
The beginnings of a module designed to wrap the PokeAPI API and consume
it easier in Python and within the Pokemon Tools library.
"""

import json
import requests


API_URI_STUB = "https://pokeapi.co/api/v2/"
CACHE_DIR = None
API_CACHE = None


class apiController:
    """An object that manages the connection between pokeapi
    (https://pokeapi.co/) and the running application."""

    def __init__(self, api_address=None, cache_path="cache.json"):
        """Initializes the apiController with default uri
        to enable HTTP requests to the API source."""
        self.cache_path = cache_path
        self.address = api_address
        self.resources = {}

    def _build_api_url(self, endpoint, resource_id=None, subresource=None):
        """Defines the full URL for the HTTP request"""
        url = "/".join((endpoint, resource_id, subresource))
        self.address = url

    def cache_resources(self):
        """Save the received resources from API call to JSON file"""
        with open(self.cache_path, "r+", encoding="utf-8") as file:
            file_data = json.load(file)

            # TODO fix this to work with resources being its own dictionary
            # Where the address is already the key to the resources
            file_data[self.address] = self.resources[self.address]

            file.seek(0)
            json.dump(file_data, file)

    def get_data(self):
        """Tries to retrieve data from the cache in case it already exists."""
        try:
            with open(API_CACHE, "r+", encoding="utf-8") as cache:
                data = json.load(cache)

            if self.address in data.keys():
                return data[self.address]

        except FileNotFoundError:
            pass

        data = self.get_resource()
        self.cache_resources()

        return data


    def get_resource(self, timeout=10):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it.

        Returns a dictionary of JSON-formatted data."""
        try:
            response = requests.get(self.address, timeout)
            response.raise_for_status()

            self.resources[self.address] = response.json()

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
