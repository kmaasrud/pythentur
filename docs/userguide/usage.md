# Usage

Accessing platforms of a stop place and all their transport calls requires knowing its identifier. This identifier can be either the platform name or its NSR ID. To get a well formatted list of the available platforms and their associated ID, you may use the `all_platforms` method.

```python
>>> oslo_s.all_platforms()
{'1': 'NSR:Quay:565',
 '10': 'NSR:Quay:551',
 '11': 'NSR:Quay:571',
 '13': 'NSR:Quay:557',
 '15': 'NSR:Quay:563',
 '16': 'NSR:Quay:562',
 '17': 'NSR:Quay:564',
 '18': 'NSR:Quay:567',
 '19': 'NSR:Quay:556',
 '3': 'NSR:Quay:554',
 '4': 'NSR:Quay:566',
 '5': 'NSR:Quay:559',
 '6': 'NSR:Quay:550',
 '7': 'NSR:Quay:553',
 '8': 'NSR:Quay:561',
 '9': 'NSR:Quay:555'}
```

From