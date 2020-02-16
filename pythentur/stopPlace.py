# Necessary imports
import requests
import json
import sys
from datetime import datetime, timezone
from .prettyTime import prettyTime

query_template = """{{
  stopPlace(id: \"{}\") {{
      name
      estimatedCalls(timeRange: 72100, numberOfDepartures: {}) {{
        aimedArrivalTime
        expectedArrivalTime
        quay {{
          publicCode
        }}
        destinationDisplay {{
          frontText
        }}
        serviceJourney {{
          journeyPattern {{
            line {{
              publicCode
            }}
          }}
        }}
      }}
    }}
  }}"""

api_url = 'https://api.entur.io/journey-planner/v2/graphql'

iso_datestring = "%Y-%m-%dT%H:%M:%S%z"

class StopPlace:
  def __init__(self, nsr_id, noDepartures = 20):
    """Initializes object with the stop's NSR ID. May also take custom GraphQL query.
    
    noDepatures - Specifies entries to retrieve. Default is 20.
    """
    self.id = nsr_id
    self.query = query_template.format(self.id, noDepartures)
    r = requests.post(api_url, json={'query': self.query}, headers={'ET-Client-Name': 'kmaasrud - pythentur'}) # TODO: Not all requests should go through me. Require custom header.
    json_data = json.loads(r.text)['data']['stopPlace']
    self.name = json_data['name'] # TODO: Not always available. Constructor must handle this.

  def get(self):
    """Retrieves list of dictionaries, containing templated data."""
    r = requests.post(api_url, json={'query': self.query}, headers={'ET-Client-Name': 'kmaasrud - pythentur'})
    json_data = json.loads(r.text)['data']['stopPlace']

    now = datetime.now(timezone.utc)
    data = []
    for call in json_data['estimatedCalls']:
      expected = datetime.strptime(call['expectedArrivalTime'], iso_datestring)
      aimed = datetime.strptime(call['aimedArrivalTime'], iso_datestring)
      data.append({
          'platform': call['quay']['publicCode'],
          'line': call['serviceJourney']['journeyPattern']['line']['publicCode']+" "+call['destinationDisplay']['frontText'],
          # TODO: Separate lineNumber and lineName
          'aimedArrivalTime': aimed,
          'expectedArrivalTime': expected,
          'delay': expected - aimed,
          'readableTime': prettyTime((expected - now).seconds)
      })

    return data

# TODO: Class handling custom route info.

if __name__ == "__main__":
  pass