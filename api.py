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

    def __init__(
        self, endpoint, resource_type, name_or_id, cache_path="cache.json"
        ):
        """Initializes the apiController with default uri
        to enable HTTP requests to the API source."""
        _name, _id = self.convert_name_or_id(endpoint, name_or_id)
        url = self._build_api_url(endpoint, resource_type, _name)
        self.__dict__ = {
            "name": _name,
            "type": resource_type,
            "endpoint": endpoint,
            "id": _id,
            "url": url}

        self.cache_path = cache_path
        self.resources = {}

        self.loaded = False

    def _build_api_url(self, endpoint, resource_id, subresource):
        """Defines the full URL for the HTTP request"""
        return "/".join((endpoint, resource_id, subresource))

    def _convert_id_to_name(self, endpoint, id_):
        """Takes the endpoint and the resource id, then
        returns the resource name as a str"""
        url = self._build_api_url(endpoint, self.__dict__["type"], id_)
        resource_data = self.get_data(url)[url]

        return resource_data.get("name", str(id_))

    def _convert_name_to_id(self, endpoint, name):
        """Takes the endpoint and the resource name, then
        returns the resource id as an int"""
        url = self._build_api_url(endpoint, self.__dict__["type"], name)
        resource_data = self.get_data(url)[url]

        return resource_data.get("id")

    def cache_resources(self):
        """Save the received resources from API call to JSON file"""
        with open(self.cache_path, "r+", encoding="utf-8") as file:
            file_data = json.load(file)

            # Iterate through saved URLs and store content with existing
            # data from cache file with key as URL if dict has data
            for (key, value) in self.resources.items():
                if value is not None:
                    file_data[key] = value

            file.seek(0)
            json.dump(file_data, file)

    def convert_name_or_id(self, endpoint, name_or_id):
        """Converts a name to an ID or an ID to a name,
        depending on type.

        Assumes ID is int and name is str."""
        if isinstance(name_or_id, int):
            id_ = name_or_id
            name = self._convert_id_to_name(endpoint, id_)
        elif isinstance(name_or_id, str):
            name = name_or_id
            id_ = self._convert_name_to_id(endpoint, name)
        else:
            raise ValueError(f"'{name_or_id}' could not be converted")

        return name, id_

    def get_data(self, url=None):
        """Tries to retrieve data from the cache in case it already exists.
        Then calls _get_resource() to send GET request to API otherwise.

        Retrieved data gets saved to self.resources as dict with url as key."""
        if url is None:
            url = self.__dict__["url"]

        try:
            with open(API_CACHE, "r+", encoding="utf-8") as cache:
                data = json.load(cache)

            if url in data.keys():
                return {url: data[url]}

        except FileNotFoundError:
            pass

        data = self._get_resource()
        self.cache_resources()

        return data

    def _get_resource(self, timeout=10):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it.

        Retrieved data gets saved to self.resources as dict with url as key."""
        resource_url = self.__dict__["url"]
        try:
            response = requests.get(resource_url, timeout)
            response.raise_for_status()

            self.resources[resource_url] = response.json()
            return {resource_url: response.json()}
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return {resource_url: None}
