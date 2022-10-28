#!/usr/bin/env python
"""
The beginnings of a module designed to wrap the PokeAPI API
and consume it easier in Python and within the Pokemon Tools library.

This module gets imported into the __init__.py file in this
directory to ease the importing process when working in adjacent
directories and for clean importing into the test suite.

For more information on this module and how it works,
please check out the __init__.py file or read the README in
the outer directory.
"""

import json
import os
import requests


API_URI_STUB = "https://pokeapi.co/api/v2"
_RESOURCE_TYPE = (
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
)


class ApiController:
    """An object that manages the connection between pokeapi
    (https://pokeapi.co/) and the running application."""

    def __init__(self, endpoint, resource_type, name_or_id):
        """Initializes the ApiController with default uri
        to enable HTTP requests to the API source."""
        self.resources = {}
        self.cache_path = self._build_cache_path()

        self.endpoint = endpoint

        self.type = self._validate_type(resource_type)

        self.name, self.id = self.convert_name_or_id(endpoint,
                                                     resource_type,
                                                     name_or_id)

        self.url = self._build_api_url(endpoint, resource_type, self.name)

    def __repr__(self):
        return f"<{self.url} - {self.name}>"

    def __str__(self):
        return f"{self.name}"

    def _build_api_url(self, endpoint, resource_type, name_or_id):
        """Defines the full URL for the HTTP request"""
        return "/".join((endpoint, resource_type, name_or_id))

    def _build_cache_path(self):
        """Finds the cwd, then builds the desired path to where
        all cached resources should be saved."""
        cache_dir = os.getcwd()
        api_cache = os.path.join(cache_dir, "cache.json")

        return api_cache

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
        if resource_type not in _RESOURCE_TYPE:
            raise ValueError(f"Unknown API endpoint '{resource_type}'")

        return resource_type

    def cache_load(self):
        """Loads the given data from the cache, if applicable.
        Handles errors that could be thrown based on the possible
        states the cache can exist in (doesn't exist, open, etc.)"""
        file_data = {}

        try:
            with open(self.cache_path, "r", encoding="utf-8") as file:
                file_data = json.load(file)
        except FileNotFoundError:
            pass
        except OSError as error:
            # Cache already open
            if error.errno == 11:
                pass
            else:
                raise error

        return file_data

    def cache_save(self):
        """Saves all held information into the cache if an identical
        cache entry doesn't already exist."""
        file_data = self.cache_load()

        try:
            for (key, value) in self.resources.items():
                if value is not None and key not in file_data.keys():
                    file_data[key] = value

            with open(self.cache_path, "w", encoding="utf-8") as file:
                file.seek(0)
                json.dump(file_data, file)
        except OSError as error:
            # Cache already open
            if error.errno == 11:
                raise KeyError("Cache could not be opened.") from error
            else:
                raise

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

        data = self.cache_load()

        if url in data.keys():
            self.resources[url] = data[url]
            return {url: data[url]}

        data = self._get_resource(url)
        self.cache_save()

        return data

    def set_cache(self, new_cache_path=None):
        """Change the cache path to new_cache_path, which can be either
        an absolute or relative path.

        If the directory does not exist, it will be created. If None is passed
        the cache will default to the cwd.

        Ensure the cache is changed BEFORE any work is done using the library,
        if at all. Otherwise errors will arise in discovering the
        cache directory during runtime."""
        if new_cache_path is None:
            new_cache_path = self._build_cache_path()

        safe_cache_dir = self.safe_make_dirs(os.path.abspath(new_cache_path))
        safe_api_cache = os.path.join(safe_cache_dir, "cache,json")

        return safe_cache_dir, safe_api_cache

    @staticmethod
    def safe_make_dirs(path, mode=0o777):
        """Create a leaf directory and all intermediate directories safely.
        Takes a path as either a relative or absolute directory tree
        to create new directories. Mode sets the directory permissions
        in octal"""
        try:
            os.makedirs(path, mode)
        except OSError as error:
            if error.errno != 17:
                # File exists
                raise

        return path


class ApiResourceList():
    """An object that connects to pokeapi (https://pokeapi.co/)
    in order to catalog resources available to the user."""

    def __init__(self, endpoint):
        """Instantiates an ApiResourceList object containing
        a list of possible resources at the given endpoint."""
        self.endpoint = endpoint
        self.cache_path = self._build_cache_path()

        # Dictionary version of results for caching
        self.response = self.get_data()
        self.cache_save()

        self._results = [i for i in self.response["results"]]
        self.count = self.response["count"]

    def __iter__(self):
        return iter(self._results)

    def __len__(self):
        return self.count

    def __str__(self):
        return f"{self._results}"

    def _build_cache_path(self):
        """Finds the cwd, then builds the desired path to where
        all cached resources should be saved."""
        cache_dir = os.getcwd()
        api_cache = os.path.join(cache_dir, "cache.json")

        return api_cache

    def _get_resource(self, timeout=10):
        """Sends a GET request to the API to receive the needed
        resource and saves it as a dict object before returning it.

        Retrieved data gets saved to self.resources as dict with url as key."""
        try:
            response = requests.get(self.endpoint, timeout=timeout)
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

    def cache_load(self):
        """Loads the given data from the cache, if applicable.
        Handles errors that could be thrown based on the possible
        states the cache can exist in (doesn't exist, open, etc.)"""
        file_data = {}

        try:
            with open(self.cache_path, "r", encoding="utf-8") as file:
                file_data = json.load(file)
        except FileNotFoundError:
            pass
        except OSError as error:
            # Cache already open
            if error.errno == 11:
                pass
            else:
                raise error

        return file_data

    def cache_save(self):
        """Saves all held information into the cache if an identical
        cache entry doesn't already exist."""
        file_data = self.cache_load()

        try:
            if (self.response is not None and
                self.endpoint not in file_data.keys()):
                file_data[self.endpoint] = self.response

            with open(self.cache_path, "w", encoding="utf-8") as file:
                file.seek(0)
                json.dump(file_data, file)
        except OSError as error:
            # Cache already open
            if error.errno == 11:
                raise KeyError("Cache could not be opened.") from error
            else:
                raise

    def get_data(self):
        """Tries to retrieve data from the cache in case it already exists.
        Then calls _get_resource() to send GET request to API otherwise.

        Retrieved data gets saved to self.resources as dict with url as key."""
        data = self.cache_load()

        if self.endpoint in data.keys():
            contents = data[self.endpoint]
        else:
            contents = self._get_resource()

        return contents


if __name__ == "__main__":
    # Quick demos if run as script instead of imported as module
    tmp = ApiController(API_URI_STUB, "pokemon", "gengar")
    print(repr(tmp))

    tmp.get_data()
    print(repr(tmp))

    new_endpoint = "/".join((API_URI_STUB, "pokemon"))
    new_tmp = ApiResourceList(new_endpoint)
    print(new_tmp)