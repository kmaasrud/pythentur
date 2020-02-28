# Pythentur

This package provides functions for simple fetching of real-time public transport data - as provided by Entur. As an added bonus, the `nsrGet`-function makes it easy to obtain the NSR ID of a stop place by a search string.

- [Pythentur](#pythentur)
  - [Installation](#installation)
  - [Usage](#usage)
    - [`StopPlace` object](#stopplace-object)
    - [`Journey` object](#journey-object)
    - [`get` method](#get-method)
      - [`StopPlace.get()`](#stopplaceget)
      - [`Journey.get()`](#journeyget)
    - [`nsrGet` function](#nsrget-function)

## Installation

```
pip install pythentur
```

or clone this GitHub repository, if you want to expand upon it.

## Usage

### `StopPlace` object

Create a `StopPlace` object by handing in the NSR ID and a header (formatted like in the example below) to the constructor.

```python
from pythentur import StopPlace
oslo_s = StopPlace("NSR:StopPlace:59872", "company - application")
```

This stores the ID, the name of the stop place (if available) and the header, for later use. 

The number of calls to retrieve can be changed by changing the keyword argument `noDepartures` in the `get` method. The default is 20.

### `Journey` object

Create a `Journey` object by handing in the NSR ID of a starting place and a destination (for now, these must be stop places, thus the NSR ID). In addition, a header is required (formatted like in the example below).

```python
from pythentur import Journey
oslo_s_to_majorstuen = Journey("NSR:StopPlace:59872", "NSR:StopPlace:58381", "company - application")
```

This stores the from and to places, along with the header and the optional keyword arguments `time` and `noDepartures`. 

`time` defaults to the current time, but a custom time is supported. The time must be a datetime object. 
<!-- TODO: Example -->
`noDepartures` is the number of journey alternatives to fetch. It defaults to 20.

### `get` method

This method is supported by both the [`StopPlace`](#stopplace-object) object and the [`Journey`](#journey-object) object. It makes a request to the Entur GraphQL API, by populating the query template with the NSR ID and the number of departures to get.

#### `StopPlace.get()`

```python
from pythentur import StopPlace
oslo_s = StopPlace("NSR:StopPlace:59872", "company - application")
data = oslo_s.get()
```

Here, `data` is a list of dictionaries, each containing:

- `'platform'`: String containing the platform this call is arriving on. May be a blank string if the stop place does not have different specified platforms.
- `'line'`: String containing the line number and name of the arriving transport.
- `'aimedArrivalTime'`: Datetime object containing the planned arrival time of the call.
- `'expectedArrivalTime'`: Datetime object containing the expected arrival time of the call.
- `'delay'`: Timedelta object containing the calculated delay of the call.
- `'readableTime'`: Returns a human readable string with relative time from now to the expected departure.

#### `Journey.get()`

```python
from pythentur import Journey
oslo_s_to_majorstuen = Journey("NSR:StopPlace:59872", "NSR:StopPlace:58381", "company - application")
data = oslo_s_to_majorstuen.get()
```

Here `data` is a list of different journey alternatives. Each of these alternatives are a list of the legs this journey has. Every leg contains
 
- `'transportMode'`: String describing the mode of transport for this leg.
- `'aimedStartTime'`: Datetime object of the aimed start time of this leg.
- `'expectedStartTime'`: Datetime object of the expected start time of this leg.
- `'fromName'`: Name of the stop place the leg starts at.
- `'fromId'`: NSR ID of the stop place the leg starts at.
- `'toName'`: Name of the stop place the leg ends at.
- `'toId'`: NSR ID of the stop place the leg ends at.
- `'lineName'`: Display name of the arriving transport (not available if `transportMode` is `foot`).
- `'lineNumber'`: Route number of the arriving transport (not available if `transportMode` is `foot`).
- `'lineColor'`: Hex color value of the arriving transport (not available if `transportMode` is `foot`).

<!-- TODO: Add some data retrieval examples. -->

### `nsrGet` function

Utilizing `nsrGet`, finding NSR IDs becomes a breeze. Hand in a search string to the function, and it spits out a list of IDs from stop places matching that string. 

<!-- TODO: Rewrite description of nsrGet function. -->