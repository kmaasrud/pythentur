# Pythentur

This package provides functions for simple fetching of real-time public transport data - as provided by Entur. As an added bonus, the `nsrGet`-function makes it easy to obtain the NSR ID of a stop place by a search string.

- [Pythentur](#pythentur)
  - [Installation](#installation)
    - [Dependencies:](#dependencies)
  - [Usage](#usage)
    - [`StopPlace` object](#stopplace-object)
    - [`StopPlace.get` method](#stopplaceget-method)
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

This stores the ID, the name of the stop place (if available) and a pre-made query template in the GraphQL format. 

The number of calls to retrieve can be changed by changing the argument `noDepartures` in the `get` method. The default is 20.

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
- `'readableTime'`: Returns a human readable string with relative time from now to the expected departure.

### `nsrGet` function

Utilizing `nsrGet`, finding NSR IDs becomes a breeze. Hand in a search string to the function, and it spits out a list of IDs from stop places matching that string. 