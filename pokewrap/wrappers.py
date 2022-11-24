"""
Generates the wrapper classes and functions used to effectively
call the api module and connect with the PokeAPI endpoint.

By utilizing these wrapper functions, classes, and values,
use of the PokeAPI becomes abstracted away behind convenient,
user-friendly function calls instead.
"""

import api


class Pokemon:
    """A Pokemon object that contains an APIController object
    with data returned from a call to the PokeAPI endpoint.
    """

    def __init__(self, name_or_id):
        """Instantiates a new Pokemon class containing an
        APIController container class with the information
        retrieved from the API or cache
        """
        self.contents = api.ApiController(
            endpoint=api.API_URI_STUB,
            resource_type="pokemon",
            name_or_id=name_or_id
        )
        self.id = self.contents.id
        self.name = self.contents.name
        self.url = self.contents.url

    def __str__(self):
        """The string representation of the object"""
        return f"{self.contents.name}"

    def __repr__(self):
        """Developer representation of the object"""
        return f"<{self.name} #{self.id} at {self.url}>"
