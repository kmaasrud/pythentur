# Welcome to Pythentur

Pythentur makes retrieving public transport data from Entur dead simple.

## Getting started

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

