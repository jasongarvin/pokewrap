"""
A quick demo of basic implementation for the pokewrap package.

Import pokewrap and create a new object, either by calling
the Pokemon wrapper class if you want a Pokemon specifically,
or by creating a new ApiController object with the resource
endpoint and type.

>>> test_mon = pokewrap.Pokemon([pokemon name or id])

or

>>> test_resource = pokewrap.ApiController([resource], [object name or id])
"""

import pokewrap


if __name__ == "__main__":
    # How to use the wrapper library
    # Get available endpoints for Pokemon
    available_resources = pokewrap.ApiResourceList("pokemon")
    print(available_resources)

    # Get resources with custom limit and/or offset
    more_available_resources = pokewrap.ApiResourceList("pokemon",
                                                        limit=100,
                                                        offset=2)

    # Create a new Pokemon object
    gengar = pokewrap.Pokemon("94")

    # Access the Pokemon name from its key in the .data dictionary
    print(gengar.data.get("name", None))
    # You can also access name, id, and uri location in the object namespace
    print(gengar.name)
    print(gengar.id)
    print(gengar.url)

    # When printed without specification, Pokemon objects default to name
    print(gengar)
