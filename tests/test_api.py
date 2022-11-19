#!/usr/bin/env python
"""A basic template to fill out with unit tests as I learn more about them.

Note that using unittest requires creating classes to run the tests
by inheriting from unittest.TestCase and prefers using its own assert
methods instead of the regular assert() call."""

# TODO: Test the remaining elements of pokewrap besides variables

import unittest
import sys
import os
import requests

# Import pokewrap/api using paths to ensure directory is found
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(MODULE_DIR)

from pokewrap import api

# Set up a test instance of ApiController for use in testing
TEST_OBJECT = api.ApiController(api.API_URI_STUB, "pokemon", "gengar")

# TODO include additional tests to ensure all global cases
# are working correctly in the pokewrap module
class TestApi(unittest.TestCase):
    """A basic test template"""

    # --- Test globals ---
    def test_api_uri(self):
        """Api uri stub in module == correct PokeAPI url"""
        api_uri = api.API_URI_STUB
        self.assertEqual(api_uri, "https://pokeapi.co/api/v2")

    # --- Test instantiation of ApiController objects ---
    def test_cache_path(self):
        """Tests that cache path loaded correctly
        into ApiController object"""
        cwd = os.getcwd()
        cache_path = os.path.join(cwd, "cache.json")
        self.assertEqual(TEST_OBJECT.cache_path, cache_path)

    def test_id(self):
        """Tests if id value is generated correctly in ApiController"""
        self.assertEqual(TEST_OBJECT.id, 94)

    def test_name(self):
        """Tests if name value is generated correctly in ApiController"""
        self.assertEqual(TEST_OBJECT.name, "gengar")

    def test_object_type(self):
        """Tests that the type of resource brought into ApiController
        exists inside RESOURCE_TYPE tuple."""
        self.assertIn(TEST_OBJECT.type, api.RESOURCE_TYPE)

    def test_resources_for_empty(self):
        """Tests that the ApiController object gets instantiated
        correctly and generates the right values."""
        self.assertNotEqual(TEST_OBJECT.resources, {})

    # --- Test API calls ---
    def test_endpoint_validity(self):
        """All endpoints in _RESOURCES are valid and return 400 code"""
        try:
            response = requests.get(api.API_URI_STUB, timeout=10)
            response.raise_for_status()
            key_set = response.json().keys()

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        self.assertTrue(set(key_set).issuperset(set(api.RESOURCE_TYPE)))


if __name__ == "__main__":
    unittest.main()
