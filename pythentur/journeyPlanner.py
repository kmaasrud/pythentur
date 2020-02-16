import requests
import json
import sys
from datetime import datetime, timezone

class Journey():
    def __init__(self, fromPlace, toPlace, header, time = None, noDepartures = 20):
        self.fromPlace = fromPlace
        self.toPlace = toPlace
        self.header = header
        self.time = time
        self.query_formatter = {'from': fromPlace, 'to': toPlace, 'noDepartures': noDepartures}

    def get(self):
        if self.time is None: self.query_formatter['time'] = datetime.now(timezone.utc).strftime(iso_datestring)
        query = query_template.format(self.query_formatter)
        r = requests.post(api_url, json={'query': query}, headers={'ET-Client-Name': self.header})
        json_data = json.loads(r.text)['data']['trip']['tripPatterns']

        data = []
        for trip in json_data:
            duration = trip['duration']
            legs = []
            for leg in trip['legs']:
                legs.append({
                    'transportMode': leg['mode'],
                    'aimedStartTime': datetime.strptime(leg['aimedStartTime'], iso_datestring),
                    'expectedStartTime': datetime.strptime(leg['expectedStartTime'], iso_datestring),
                    'lineName': leg['fromEstimatedCall']['destinationDisplay']['frontText'],
                    'lineNumber': leg['line']['publicCode'],
                    'lineColor': "#" + leg['line']['presentation']['colour'],
                    'fromName': leg['fromPlace']['quay']['stopPlace']['name'],
                    'fromId': leg['fromPlace']['quay']['stopPlace']['id'],
                    'toName': leg['toPlace']['quay']['stopPlace']['name'],
                    'toId': leg['toPlace']['quay']['stopPlace']['id']
                })
            data.append({'duration': duration, 'legs': legs})
        
        return data

# TODO: Preferred or banned transport modes.
query_template = """{{
  trip(
    from: {{
      place: {from}
    }}
    to: {{
      place: {to}
    }}
    numTripPatterns: {noDepartures}
    dateTime: {time}
    minimumTransferTime: 180
  )

#### Requested fields
  {{
    tripPatterns {{
      duration
      legs {{
        mode
        aimedStartTime
        expectedStartTime
        fromEstimatedCall {{
          destinationDisplay {{
            frontText
          }}
        }}
        line {{
          publicCode
          name
          presentation {{
            colour
          }}
        }}
        fromPlace{{
          quay {{
            stopPlace {{
              name
              id
            }}
          }}
        }}
        toPlace {{
          quay {{
            stopPlace {{
              name
              id
            }}
          }}
        }}
      }}
    }}
  }}
}}"""

api_url = 'https://api.entur.io/journey-planner/v2/graphql'

iso_datestring = "%Y-%m-%dT%H:%M:%S%z"