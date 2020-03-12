from requests import post
import json
from datetime import datetime, timezone

from . import StopPlace
from .helpers import ISO_FORMAT, API_URL, QUERY_JOURNEY
from .helpers import post_to_api

class Journey():
    """Object containing a journey from one place to another.

    Args:
        fromPlace (str): NSR ID of stop place to travel from.
        toPlace (str): NSR ID of stop place to travel to.
        header (str): Header string in the format 'company - application'

    Keyword args:
        time (datetime): Time of departure, as a datetime object. (default: now)
        noDepartures (int): Number of routes to fetch. (default: 20)
    """
    def __init__(self, fromPlace, toPlace, header, time = datetime.now(timezone.utc)):
        self._from = fromPlace
        self.fromPlace = fromPlace.name
        self._to = toPlace
        self.toPlace = toPlace.name
        self.header = header
        self.time = time.strftime(ISO_FORMAT)
        self.n_trips = 20
        self.trips = [None] * self.n_trips

    @classmethod
    def from_string(cls, fromPlace, toPlace, header, time = datetime.now(timezone.utc)):
        from_ = StopPlace.from_string(fromPlace, header)
        to_ = StopPlace.from_string(toPlace, header)

        return cls(from_, to_, header, time = time)

    def trip(self, i):
        query = QUERY_JOURNEY.format(**{
            'from': self._from.id, 'to': self._to.id,
            'time': self.time, 'noDepartures': self.n_trips
            })
        r = post(API_URL,
            json={'query': query},
            headers={'ET-Client-Name': self.header}
        )
        data = json.loads(r.text)['data']

        duration = data['duration']
        legs = []
        for leg in data['legs']:
            if leg['mode'] == 'foot':
                legs.append({
                    'transportMode': leg['mode'],
                    'aimedStartTime': datetime.strptime(leg['aimedStartTime'], ISO_FORMAT),
                    'expectedStartTime': datetime.strptime(leg['expectedStartTime'], ISO_FORMAT),
                    'fromName': leg['fromPlace']['quay']['stopPlace']['name'], # TODO: Needs a fix for when the departure place is not a stop place.
                    'fromId': leg['fromPlace']['quay']['stopPlace']['id'], # TODO: See above
                    'toName': leg['toPlace']['quay']['stopPlace']['name'], # TODO: See above
                    'toId': leg['toPlace']['quay']['stopPlace']['id'] # TODO: See above
                })
            else:
                legs.append({
                    'transportMode': leg['mode'],
                    'aimedStartTime': datetime.strptime(leg['aimedStartTime'], ISO_FORMAT),
                    'expectedStartTime': datetime.strptime(leg['expectedStartTime'], ISO_FORMAT),
                    'lineName': leg['fromEstimatedCall']['destinationDisplay']['frontText'],
                    'lineNumber': leg['line']['publicCode'],
                    'lineColor': "#" + leg['line']['presentation']['colour'],
                    'fromName': leg['fromPlace']['quay']['stopPlace']['name'],
                    'fromId': leg['fromPlace']['quay']['stopPlace']['id'],
                    'toName': leg['toPlace']['quay']['stopPlace']['name'],
                    'toId': leg['toPlace']['quay']['stopPlace']['id']
                })

        self.trips[i] = {'duration': duration, 'legs': legs}

        return self.trips[i]

    def __getitem__(self, i):
        return self.trip(i)

# TODO: Preferred or banned transport modes.

if __name__ == "__main__":
    pass