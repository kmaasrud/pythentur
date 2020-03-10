# Welcome to Pythentur

Pythentur makes retrieving public transport data from Entur dead simple.

## Getting started

- [Welcome to Pythentur](#welcome-to-pythentur)
  - [Getting started](#getting-started)
- [Installation](#installation)
- [Quickstart](#quickstart)

# Installation

Install using pip

```
pip install pythentur
```

or clone the [GitHub repository](https://github.com/kmaasrud/pythentur) and install locally.

# Quickstart

Here's how to get data about the first incoming transport from platform H of the stop place Majorstuen:

```python
>>> from pythentur import StopPlace
>>> header = 'company - application'
>>> majorstuen = StopPlace.from_string('Majorstuen', header)
>>> majorstuen['H'][0]
{
    'aimed': datetime.datetime(2020, 3, 9, 19, 25, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))),
    'expected': datetime.datetime(2020, 3, 9, 19, 25, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))),
    'line': 'FB1',
    'destination': 'Oslo lufthavn',
    'delay': datetime.timedelta(0),
    'readableTime': '1 minute'
}
```

As you can see, Entur requires every user of its API to identify themselves through a header. Just pass the name of your company and application (in the format shown above) to the constructor.

Every platform of a stop place is accessed through their name, or - in the case of the platform not having a name - through their NSR (National Stopplace Registry) quay ID. Every platform and their names can be listed like this:

```
>>> majorstuen.platforms
[NSR:Quay:103697, 2, C, J, F, 4, NSR:Quay:102441, NSR:Quay:8113, NSR:Quay:102319, NSR:Quay:8078, NSR:Quay:103698, NSR:Quay:101740, B, A, NSR:Quay:8115, E, G, 1, NSR:Quay:8077, D, C, A, H]
```

The transport calls from each platform are accessed through the corresponding index, and are always up to date when you access them. 