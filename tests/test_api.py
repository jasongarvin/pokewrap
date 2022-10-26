"""A basic template to fill out with unit tests as I learn more about them.

Note that using unittest requires creating classes to run the tests
by inheriting from unittest.TestCase and prefers using its own assert
methods instead of the regular assert() call."""

import unittest
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(MODULE_DIR)

from pokewrap import api

# TODO include additional tests to ensure all global cases
# are working correctly in the pokewrap module
class TestGlobals(unittest.TestCase):
    """A basic test template"""

    def test_api_uri(self):
        """Api uri stub in module == correct PokeAPI url"""
        api_uri = api.API_URI_STUB
        self.assertEqual(api_uri, "https://pokeapi.co/api/v2")


if __name__ == "__main__":
    unittest.main()
