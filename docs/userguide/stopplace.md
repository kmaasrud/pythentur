# The `StopPlace` object

Every stop place in the National Stop Register can become a Python-friendly `StopPlace`. Every `StopPlace` contains a number of [`Platform`s](platform.md), which are the main interface to fetch transport data.

`StopPlace` is a subclass of [`Location`](location.md) and does thus contain geographic data like coordinates and locality. This is further explained in [the Location docs](location.md#attributes).

# Attributes

| Attribute        | Description                 |
| :--------- | :-------------------------- |
| `StopPlace.name` | The name of the stop place. |
| `StopPlace.id` | The NSR ID of the stop place. |
| `StopPlace.platforms` | List of all the stop place's platforms. Each of these platforms are a [`Platform`](platform.md) object, and can be accessed through their `name` or their `id`. |
| `StopPlace.zones` | The tariff zones the stop place is a part of. |