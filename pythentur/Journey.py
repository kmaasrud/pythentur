import requests
import json
from datetime import datetime, timezone
from .constants import QUERY_JOURNEY, API_URL, ISO_FORMAT

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
    def __init__(self, fromPlace, toPlace, header, time = None, noDepartures = 20):
        self.fromPlace = fromPlace
        self.toPlace = toPlace
        self.header = header
        self.time = time
        self.query_formatter = {'from': fromPlace, 'to': toPlace, 'noDepartures': noDepartures}

    def get(self):
        if self.time is None: self.query_formatter['time'] = datetime.now(timezone.utc).strftime(ISO_FORMAT)
        else: self.query_formatter['time'] = self.time.strftime(ISO_FORMAT)
        query = QUERY_JOURNEY.format(**self.query_formatter)
        r = requests.post(API_URL, json={'query': query}, headers={'ET-Client-Name': self.header})
        json_data = json.loads(r.text)['data']['trip']['tripPatterns']

        data = []
        for trip in json_data:
            duration = trip['duration']
            legs = []
            for leg in trip['legs']:
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
                # TODO: Add waiting time to legs.
                # TODO: Add readable time to legs.
            data.append({'duration': duration, 'legs': legs})

        return data

# TODO: Preferred or banned transport modes.

if __name__ == "__main__":
    pass