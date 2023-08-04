# Pokewrap 0.0.3

A wrapper library for the PokeAPI making it easier to build into other python scripts through a quick import.

By relying on objects to handle communicating with the API and parsing data into meaningful chunks, pokewrap ensures a smooth experience working with the returned json. Pokewrap uses objects to wrap the returned json, ensuring more meaningful access to the data contained therein.

You can use Pokewrap to connect with the API endpoint and request specific bits of data without having to worry about the response format. You can also use it to see which endpoints are available if you're unsure where to start or need to generate a way to pull from several endpoints.

## Getting Started

* Coming soon the package will be available on PyPi, but there needs to be more written tests to ensure it's stable first. When that happens you'll be able to install with pip, but for now please clone or download the package from github itself.

---

To use Pokewrap, first import it into your script or service:

```python
import pokewrap
```

From there, you can start making requests using the ApiController class or choose a resource-specific wrapper (currently only available for Pokemon).

Set up the class by specifying as str the type of resource and the specific resource, or as int the Pokemon ID number.

For example, to see the Pokemon Gengar and its information, set:

```python
ApiController("pokemon", "gengar")
```

Or, using the ID:

```python
ApiController("pokemon", 94)
```

If you'd prefer to use the wrapper class Pokemon, you can simply request information for a Pokemon in the following way:

```python
Pokemon('gengar')   #Using the name
Pokemon(94)         #Using the ID
```

You can also use ApiResourceList to get a dictionary response of all viable resources within a supertype (or access the global variable RESOURCE_ENDPOINTS).

For example, to see every Pokemon available through the endpoint:

```python
ApiResourceList("pokemon")
```

Note that the default limit is 20 for resource requests. This should become configurable in the future.

For a conprehensive list of all available resource types, check the static RESOURCE_TYPE variable or the dynamically-generated RESOURCE_ENDPOINTS variable.

## Coming Soon

* I'll be honest. I got incredibly busy with other projects, consulting, and business acquisition. This library was meant as a learning experience so I don't have immediate plans to update it in major ways. I fully intend to come back and clean up some edge cases, but haven't thus far.

* Below you'll find the features I indend to add, but there is no longer a clear timeline.

The goal is to eventually support custom limit and offset values in your http requests. I'll also continue expanding the functionalities of this module as the need arises (bug fixes as well, where applicable).

pokewrap will also grow to include more comprehensive testing and data validation, to ensure no matter what your request and its context that Pokewrap still gives you the best result for your use case.
