# Pythentur

> Entur data-fetch in Python

This package provides functions for simple fetching of real-time public transport data - as provided by Entur. As an added bonus, the `nsrGet`-function makes it easy to obtain the NSR ID of a stop place by a search string.

- [Pythentur](#pythentur)
  - [Installation](#installation)
    - [Dependencies:](#dependencies)
  - [Usage](#usage)
    - [`StopPlace` object](#stopplace-object)
    - [`StopPlace.get()` method](#stopplaceget-method)

## Installation

`pip install pythentur`

### Dependencies:
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

### `StopPlace.get()` method

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

The number of calls to retrieve can be changed by changing the argument `noDepartures` in the `get()` method. The default is 20.