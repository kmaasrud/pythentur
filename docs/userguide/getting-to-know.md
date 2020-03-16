# Getting to know the object types

## `Location`

### Constructing

### <a name="la"></a>Attributes

## `StopPlace`

Every stop place in the National Stop Register (NSR) can become a Python-friendly `StopPlace`. Every `StopPlace` contains a number of [`Platforms`](#platform), which are the main interface to fetch transport data.

!!! info
    `StopPlace` is a subclass of [`Location`](#location) and does thus contain geographic data like coordinates and locality. This is further explained in [The Location Object](#la).

### Constructing

To construct a `StopPlace`, you need the NSR stop place ID and Entur's required `"ET-Client-Name"` header.

- The NSR ID is easily found by searching for the requested stop place on [Entur's travel planner](https://entur.no/avgangstavle) and checking the URL. An alternative is using [`from_string`](#using-from_string) to construct the class instead.
- The header is required by Entur to identify any users of their API. Omitting this deploys rate-limiting, and is therefore not supported by this package. The format of the header should be `"company - application"`.

As an example,

```python
from pythentur import StopPlace

oslo_s = StopPlace(
    'NSR:StopPlace:59872', header = 'foo_company - bar_app'
)
```

would make `oslo_s` a `StopPlace` object for Oslo Central Station.

!!! info
    For larger stop places with many platforms, initializing a `StopPlace` might take a few seconds, since the API is queried for each platform. However, when the `StopPlace` is loaded in memory, the operations should be quite snappy.

#### Using `from_string`

To avoid having to look up the NSR ID of a stop place, an alternative way of constructing a `StopPlace` is supplied. `from_string` takes a searchstring and the `"ET-Client-Name"` header as parameters, and returns the first stop place matching that string.

```python
from pythentur import StopPlace

nationaltheatret = StopPlace.from_string(
    'nationaltheatret', header = 'foo_company - bar_app'
)
```

### Attributes

| Attribute  | Description |
| :--------- | :-------------------------- |
| `name` | The name of the stop place. |
| `id` | The NSR ID of the stop place. |
| `platforms` | List of all the stop place's platforms. Each of these platforms are a [`Platform`](#platform) object, and can be accessed with their `name` or  `id` as a key. |
| `zones` | A list of the tariff zones the stop place is a part of. |

In addition, `StopPlace` contains all of the attributes of the [`Location`](#la) class.

## `Platform`