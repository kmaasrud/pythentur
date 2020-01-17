# Necessary imports
import requests
import json
import sys
from datetime import datetime

# Not necessary
import pprint

query_template = """{{
    stopPlace(id: "{}") {{
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

query_url = 'https://api.entur.io/journey-planner/v2/graphql'

iso_datestring = "%Y-%m-%dT%H:%M:%S%z"

class Stop:
  def __init__(self, nsr_id, query = query_template):
    """Initializes object with the stop's NSR ID. May also take custom GraphQL query."""
    self.id = nsr_id
    self.query = query

  def get(self, noDepartures = 20):
    """Retrieves list of dictionaries, containing templated data. 
    noDepatures specifies entries to retrieve, default is 20."""

    self.query = self.query.format(self.id, noDepartures)
    r = requests.post(query_url, json={'query': self.query}, headers={"ET-Client-Name": "kmaasrud - entur-py"})
    json_data = json.loads(r.text)['data']['stopPlace']

    self.name = json_data['name']
    data = []

    for call in json_data['estimatedCalls']:
      aimed = datetime.strptime(call['aimedArrivalTime'], iso_datestring)
      expected = datetime.strptime(call['expectedArrivalTime'], iso_datestring)
      delay = expected - aimed
      line = call['serviceJourney']['journeyPattern']['line']['publicCode']+" "+call['destinationDisplay']['frontText']
      platform = call['quay']['publicCode']

      dictio = {
          'platform': platform,
          'line': line,
          'aimedArrivalTime': aimed,
          'expectedArrivalTime': expected,
          'delay': delay
      }

      data.append(dictio)

    return data

  def getCustom(self, noDepartures = 20):
    """Retrieves list of dictionaries, containing data from custom query. 
    noDepatures specifies entries to retrieve, default is 20."""

    self.query = self.query.format(self.id, noDepartures)
    r = requests.post(query_url, json={'query': self.query}, headers={"ET-Client-Name": "kmaasrud - entur-py"})
    json_data = json.loads(r.text)['data']['stopPlace']

    self.name = json_data['name']

    return json_data['estimatedCalls']


if __name__ == "__main__":
  query = query_template.format("NSR:StopPlace:337", 20)
  r = requests.post(query_url, json={'query': query}, headers={"ET-Client-Name": "kmaasrud - entur-py"})
  json_data = json.loads(r.text)
  print(json_data)