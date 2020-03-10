# Welcome to Pythentur

Pythentur makes retrieving public transport data from Entur dead simple.

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
>>> header = '<company> - <application>'
>>> majorstuen = StopPlace.from_string('Majorstuen', header)
>>> majorstuen['G'][0]
{
  'line': '46',
  'destination': 'Ullerntoppen',
  'aimed': datetime.datetime(2020, 3, 10, 12, 48, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))),
  'expected': datetime.datetime(2020, 3, 10, 12, 48, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))),
  'delay': datetime.timedelta(0),
  'readableTime': '2 minutes'
}
```

Entur requires every user of its API to identify themselves through a header. Just pass the name of your company and application (in the format shown above) to the constructor.

Every platform of a stop place is accessed through their name, or - in the case of the platform not having a name - through their NSR (National Stop Register) quay ID. Every platform can be listed like this:

```
>>> majorstuen.platforms
[NSR:Quay:8079, NSR:Quay:8027, NSR:Quay:102023, NSR:Quay:8066,
NSR:Quay:8089, NSR:Quay:8042, NSR:Quay:8028, NSR:Quay:8050,
NSR:Quay:8051, NSR:Quay:104056, NSR:Quay:8076, NSR:Quay:8058,
NSR:Quay:8067]
```

This isn't too easy to decode, obviously, but a quick check on [Entur](https://entur.no/avgangstavle) should show you which platforms are on each stop in a more human-friendly manner. 

The transport calls from each platform are accessed through the corresponding index, and are always up to date when you access them. For example, accessing the first element of platform G twice always gives me the result at that specific time.

```python
>>> majorstuen['1'][0]['destination']
'Ellingsrudåsen'
>>> majorstuen['1'][0]['destination']
'Mortensrud'
```

For the time being, the list of calls is limited to 20 elements. This should however suffice for most cases.