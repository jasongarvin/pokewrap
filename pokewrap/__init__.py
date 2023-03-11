#!/usr/bin/env python

"""
pokewrap
A small Python wrapper for PokeAPI (https://pokeapi.co)

Usage:
>>> import pokewrap
>>> clientV2 = pokepy.V2Client()
>>> clientV2.get_pokemon('bulbasaur')
<Pokemon - Bulbasaur>
"""

__author__ = "Jason Garvin"
__email__ = "jsongarvin@gmail.com"
__version__ = "0.0.3"
__copyright__ = "Copyright Jason Garvin 2023"
__license__ = "BSD"


from .api import API_URI_STUB, RESOURCE_ENDPOINTS, RESOURCE_TYPES
from .api import ApiController, ApiResourceList
from .wrappers import Pokemon
