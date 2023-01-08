# Pokewrap
A wrapper library for the PokeAPI making it easier to build into other python scripts through a quick import.

By relying on objects to handle communicating with the AP and parsing data into meaningful chunks, pokewrap ensures a smooth experience working with the returned JSON. Pokewrap uses objects to wrap the returned json, ensuring more meaningful access to the data contained therein. 

You can use Pokewrap to connect with the API endpoint and request specific bits of data without having to worry about the response format.

## Getting Started
To use Pokewrap, first import it into your script or service:

```
import pokewrap
```

From there, you can start making requests using the ApiController class.

Set up the class by specifying as str the type of resource and the specific resource.

For example, to see the Pokemon Gengar and its information, set:

```
ApiController("pokemon", "gengar")
```

You can also use ApiResourceList to get a dictionary response of all viable resources within a supertype.

For example, to see every Pokemon available through the endpoint:

```
ApiResourceList("pokemon")
```

Note that the default limit is 20 for resource requests. In the future Pokewrap will support manually setting the limit and offset of your request to ensure you get all the information you need on the first try.

For a conprehensive list of all available resource types, check the static variable RESOURCE_TYPE.

## Coming Soon

As mentioned above, the goal is to eventually support custom limit and offset values in your http requests.

Pokewrap will also grow to include more comprehensive testing and data validation, to ensure no matter what your request and its context that Pokewrap still gives you the best result for your use case.
