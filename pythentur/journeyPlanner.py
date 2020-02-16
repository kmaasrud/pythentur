import requests
import json
import sys
from datetime import datetime

class Journey():
    def __init__(self, fromPlace, toPlace, header, time = None, noDepartures = 20):
        self.time = time
        self.query_formatter = {'from': fromPlace, 'to': toPlace, 'noDepartures': noDepartures}

    def get(self):
        query = query_template.format(self.query_formatter)
        r = requests.post(api_url, json={'query': query}, headers={'ET-Client-Name': 'kmaasrud - pythentur'})
        json_data = json.loads(r.text)['data']

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