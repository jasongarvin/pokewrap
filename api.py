"""
The beginnings of a module designed to wrap the PokeAPI API and consume
it easier in Python and within the Pokemon Tools library.
"""

import json
import os
import requests


# TODO Write Unit Tests and Integration Tests to ensure everything works
API_URI_STUB = "https://pokeapi.co/api/v2"
CACHE_DIR = os.getcwd()
API_CACHE = os.path.join(CACHE_DIR, "cache.json")
RESOURCE_TYPE = [
    "ability",
    "berry",
    "berry-firmness",
    "berry-flavor",
    "characteristic",
    "contest-effect",
    "contest-type",
    "egg-group",
    "encounter-condition",
    "encounter-condition-value",
    "encounter-method",
    "evolution-chain",
    "evolution-trigger",
    "gender",
    "generation",
    "growth-rate",
    "item",
    "item-attribute",
    "item-category",
    "item-fling-effect",
    "item-pocket",
    "language",
    "location",
    "location-area",
    "machine",
    "move",
    "move-ailment",
    "move-battle-style",
    "move-category",
    "move-damage-class",
    "move-learn-method",
    "move-target",
    "nature",
    "pal-park-area",
    "pokeathlon-stat",
    "pokedex",
    "pokemon",
    "pokemon-color",
    "pokemon-form",
    "pokemon-habitat",
    "pokemon-shape",
    "pokemon-species",
    "region",
    "stat",
    "super-contest-effect",
    "type",
    "version",
    "version-group",
]


class apiController:
    """An object that manages the connection between pokeapi
    (https://pokeapi.co/) and the running application."""

    def __init__(
        self, endpoint, resource_type, name_or_id, cache_path=API_CACHE
        ):
        """Initializes the apiController with default uri
        to enable HTTP requests to the API source."""
        self.resources = {}
        self.cache_path = cache_path

        self.endpoint = endpoint
        self.type = self._validate_type(resource_type)
        self.name, self.id = self.convert_name_or_id(endpoint,
                                                     resource_type,
                                                     name_or_id)
        self.url = self._build_api_url(endpoint, resource_type, self.name)

    # Overloading built-in object methods
    def __repr__(self):
        return f"<{self.url} - {self.name}>"

    def __str__(self):
        return f"{self.name}"

    # Private methods that don't need to be called directly
    def _build_api_url(self, endpoint, resource_type, name_or_id):
        """Defines the full URL for the HTTP request"""
        return "/".join((endpoint, resource_type, name_or_id))

    def _convert_id_to_name(self, endpoint, resource_type, id_):
        """Takes the endpoint and the resource id, then
        returns the resource name as a str"""
        url = self._build_api_url(endpoint, resource_type, id_)
        resource_data = self.get_data(url)

        return resource_data[url].get("name", str(id_))

    def _convert_name_to_id(self, endpoint, resource_type, name):
        """Takes the endpoint and the resource name, then
        returns the resource id as an int"""
        url = self._build_api_url(endpoint, resource_type, name)
        resource_data = self.get_data(url)

        return resource_data[url].get("id")

    def _get_resource(self, url=None, timeout=10):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it.

        Retrieved data gets saved to self.resources as dict with url as key."""
        if url is None:
            url = self.url
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            self.resources[url] = response.json()
            return {url: response.json()}
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return {url: None}

    def _validate_type(self, resource_type):
        """Checks if the endpoint is a valid API endpoint within PokeAPI.
        Raises error if endpoint not in the list of valid resource types"""
        if resource_type not in RESOURCE_TYPE:
            raise ValueError(f"Unknown API endpoint '{resource_type}'")

        return resource_type

    # Callable methods used by the public consumer of the library
    def cache_resources(self):
        """Save the received resources from API call to JSON file"""
        file_data = {}

        if os.path.exists(API_CACHE):
            with open(self.cache_path, "r", encoding="utf-8") as file:
                file_data = json.load(file)

        # Add new resources to file_data in addition to imported data
        # Avoiding duplicates, to ensure the cache properly tracks resources
        for (key, value) in self.resources.items():
            if value is not None and key not in file_data.keys():
                file_data[key] = value

        with open(self.cache_path, "w", encoding="utf-8") as file:
            file.seek(0)
            json.dump(file_data, file)

    def convert_name_or_id(self, endpoint, resource_type, name_or_id):
        """Converts a name to an ID or an ID to a name,
        depending on type.

        Assumes ID is int and name is str."""
        if isinstance(name_or_id, int):
            id_ = name_or_id
            name = self._convert_id_to_name(endpoint, resource_type, id_)

        elif isinstance(name_or_id, str):
            name = name_or_id
            id_ = self._convert_name_to_id(endpoint, resource_type, name)

        else:
            raise ValueError(f"'{name_or_id}' could not be converted")

        return name, id_

    def get_data(self, url=None):
        """Tries to retrieve data from the cache in case it already exists.
        Then calls _get_resource() to send GET request to API otherwise.

        Retrieved data gets saved to self.resources as dict with url as key."""
        if url is None:
            url = self.url

        try:
            with open(API_CACHE, "r+", encoding="utf-8") as cache:
                data = json.load(cache)

            if url in data.keys():
                self.resources[url] = data[url]
                self.cache_resources()
                return {url: data[url]}

        except FileNotFoundError:
            pass

        data = self._get_resource(url)
        self.cache_resources()

        return data


class apiResourceList():
    """An object that connects to pokeapi (https://pokeapi.co/)
    in order to catalog resources available to the user."""

    def __init__(self, endpoint):
        """Instantiates an apiResourceList object containing
        a list of possible resources at the given endpoint."""
        response = self.get_data(endpoint)

        self.name = endpoint
        self._results = [i for i in response["results"]]
        self.count = response["count"]

    # Overloading built-in object methods
    def __iter__(self):
        return iter(self._results)

    def __len__(self):
        return self.count

    def __str__(self):
        return f"{self._results}"

    # Private methods that don't need to be called directly
    def _get_resource(self, url, timeout=10):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it.

        Retrieved data gets saved to self.resources as dict with url as key."""
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return {}

    # Callable methods used by the public consumer of the library
    def get_data(self, url):
        """Tries to retrieve data from the cache in case it already exists.
        Then calls _get_resource() to send GET request to API otherwise.

        Retrieved data gets saved to self.resources as dict with url as key."""
        try:
            with open(API_CACHE, "r+", encoding="utf-8") as cache:
                data = json.load(cache)

            if url in data.keys():
                return data[url]

        except FileNotFoundError:
            pass

        data = self._get_resource(url)
        return data
