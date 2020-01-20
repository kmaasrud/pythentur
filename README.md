# Pythentur

This package provides functions for simple fetching of real-time public transport data - as provided by Entur. As an added bonus, the `nsrGet`-function makes it easy to obtain the NSR ID of a stop place by a search string.

- [Pythentur](#pythentur)
  - [Installation](#installation)
    - [Dependencies:](#dependencies)
  - [Usage](#usage)
    - [`StopPlace` object](#stopplace-object)
    - [`StopPlace.get` method](#stopplaceget-method)
    - [`StopPlace.getCustom` method](#stopplacegetcustom-method)
    - [`nsrGet` function](#nsrget-function)

## Installation

`pip install pythentur`

### Dependencies:

Due to an issue, I'm not able to generate package dependencies, so they will have to be installed manually for the time being.

- Requests

## Usage

### `StopPlace` object

Create a `StopPlace` object by handing in the NSR ID to the constructor.

```
from pythentur import StopPlace
oslo_s = StopPlace("NSR:StopPlace:59872")
```

This stores the ID and a pre-made query template in the GraphQL format. 

Pythentur supports custom query templates, if you wish to retrieve more data. This is given to the constructor with the `query` argument.

    query_template = "<graphQL query>"
    oslo_s = StopPlace("NSR:StopPlace:59872", query = query_template)

This template string must have two spots (for the NSR ID and the number of calls to recieve) that are formattable by the Python `format` method. The GraphQL interface can be experimented with [here.](https://api.entur.io/journey-planner/v2/ide/?query=%7B%0A%20%20stopPlace(id%3A%20%22NSR%3AStopPlace%3A337%22)%20%7B%0A%20%20%20%20name%0A%20%20%20%20id%0A%20%20%20%20estimatedCalls%20%7B%0A%20%20%20%20%20%20expectedDepartureTime%0A%20%20%20%20%20%20destinationDisplay%20%7B%0A%20%20%20%20%20%20%20%20frontText%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20serviceJourney%20%7B%0A%20%20%20%20%20%20%20%20line%20%7B%0A%20%20%20%20%20%20%20%20%20%20publicCode%0A%20%20%20%20%20%20%20%20%20%20transportMode%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

### `StopPlace.get` method

This method makes a request to the Entur GraphQL API, by populating the query template with the NSR ID and the number of calls to get. This retrieves a list of calls, each represented by a dictionary.

    from pythentur import StopPlace
    oslo_s = StopPlace("NSR:StopPlace:59872")
    data = oslo_s.get()

Here, `data` is a list of dictionaries, each containing:

- `'platform'`: String containing the platform this call is arriving on. May be a blank string if the stop place does not have different specified platforms.
- `'line'`: String containing the line number and name of the arriving transport.
- `'aimedArrivalTime'`: Datetime object containing the planned arrival time of the call.
- `'expectedArrivalTime'`: Datetime object containing the expected arrival time of the call.
- `'delay'`: Timedelta object containing the calculated delay of the call.

The number of calls to retrieve can be changed by changing the argument `noDepartures` in the `get` method. The default is 20.

In addition to getting the departure data for the stop, `get` also fetches the name of the stop and stores it in a variable `name`.

### `StopPlace.getCustom` method

Given a custom query, the `get` method will (probably) not work. In this case, the `getCustom` method should be used, and will return the resulting json data back as a dictionary.

### `nsrGet` function

Utilizing `nsrGet`, finding NSR IDs becomes a breeze. Hand in a search string to the function, and it spits out a list of IDs from stop places matching that string. 