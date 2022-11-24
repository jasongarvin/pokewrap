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

        self.dict = self._build_dict()

        self.abilities = self.dict.get("abilities", {})
        self.base_exp = self.dict.get("base_experience", {})
        self.encounters = self.dict.get("location_area_encounters", {})
        self.forms = self.dict.get("forms", {})
        self.game_indices = self.dict.get("game_indices", {})
        self.height = self.dict.get("height", {})
        self.held_items = self.dict.get("held_items", {})

        self.id = self.contents.id

        self.is_default = self.dict.get("is_default", {})
        self.moves = self.dict.get("moves", {})

        self.name = self.contents.name

        self.order = self.dict.get("order", {})
        self.past_types = self.dict.get("past_types", {})
        self.species = self.dict.get("species", {})
        self.sprites = self.dict.get("sprites", {})
        self.stats = self.dict.get("stats", {})
        self.types = self.dict.get("types", {})

        self.url = self.contents.url

        self.weight = self.dict.get("weight", {})

    def __str__(self):
        """The string representation of the object"""
        return f"{self.contents.name}"

    def __repr__(self):
        """Developer representation of the object"""
        return f"<{self.name} #{self.id} at {self.url}>"

    def _build_dict(self):
        """Returns a dictionary object from further inside
        the nested dict structure returned from the API call
        """
        # TODO make this less hacky
        big_key = [key for key in self.contents.resources.keys()][0]
        new_dict = {key: self.contents.resources[big_key][key]
                    for key in self.contents.resources[big_key].keys()}

        return new_dict


if __name__ == "__main__":
    test = Pokemon("gengar")
