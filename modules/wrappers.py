"""
Generates the wrapper classes and functions used to effectively
call the api module and connect with the PokeAPI endpoint.

By utilizing these wrapper functions, classes, and values,
use of the PokeAPI becomes abstracted away behind convenient,
user-friendly function calls instead.

Create a new Pokemon object with just the Pokemon name or ID:
>>> poke = Pokemon("gengar")
>>> print(poke)
"gengar"

Then access its data using dictionary keys from .content:
>>> poke.content["types"]
"types": [
    {
        "slot": 1,
        "type": {
            "name": "ghost",
            "url": "https://pokeapi.co/api/v2/type/8/"
        }
    },
    {
        "slot": 2,
        "type": {
            "name": "poison",
            "url": "https://pokeapi.co/api/v2/type/4/"
        }
    }
"""

from pprint import pprint

from api import ApiController


class Pokemon:
    """A Pokemon object that contains an APIController object
    with data returned from a call to the PokeAPI endpoint.
    """

    def __init__(self, name_or_id):
        """Instantiates a new Pokemon class containing an
        APIController container class with the information
        retrieved from the API or cache
        """
        self._api_data = ApiController(
            resource_type="pokemon",
            name_or_id=name_or_id
        )

        self.content = self._build_dict()
        self.id = self._api_data.id
        self.name = self._api_data.name
        self.url = self._api_data.url

    def __str__(self):
        return f"{self.content.name}"

    def __repr__(self):
        return f"<{self.name} #{self.id} at {self.url}>"

    def _build_dict(self):
        """Returns a dictionary object from further inside
        the nested dict structure returned from the API call.
        """
        # Specifically needs to be an indexable list (keys object is not)
        all_keys = [key for key in self._api_data.resources]

        if len(all_keys) == 1:
            big_key = all_keys[0]
            new_dict = {key: self._api_data.resources[big_key][key]
                        for key in self._api_data.resources[big_key].keys()}
        else:
            new_dict = {}
            for big_key in all_keys:
                t_dict = {key: self._api_data.resources[big_key][key]
                          for key in self._api_data.resources[big_key].keys()}
                new_dict[big_key] = t_dict

        return new_dict


if __name__ == "__main__":
    test = Pokemon("gengar")
    pprint(test.content)
