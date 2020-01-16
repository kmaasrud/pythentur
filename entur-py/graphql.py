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

iso_datestring = "%Y-%m-%dT%H:%M:%s%z"

class Stop:
  def __init__(self, nsr_id, query = query_template):
    """Initializes object with the stop's NSR ID. May also take custom GraphQL query."""
    self.id = nsr_id
    self.query = query

  def get(self, noDepartures = 20):
    self.query.format(self.id, noDepartures)
    r = requests.post(query_url, json={'query': self.query}, headers={"ET-Client-Name": "kmaasrud - entur-py"})
    self.json_data = json.loads(r.text)['data']['stopPlace']

    self.name = self.json_data['name']
    self.data = []

    for call in self.json_data['estimatedCalls']:
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
      
      self.data.append(dictio)



def realtime_data(stops):
  """Returns dictionary of realtime transport data from list of Entur stop id's"""

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

  url = 'https://api.entur.io/journey-planner/v2/graphql'

  stops_data = {}
  for i in range(len(stops)):
    query = query_template.format(stops[i])
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)['data']['stopPlace']
    name = json_data['name']

    s = []
    for call in json_data['estimatedCalls']:
        dictio = {
            'platform': call['quay']['publicCode'],
            'line': call['serviceJourney']['journeyPattern']['line']['publicCode']+" "+call['destinationDisplay']['frontText'],
            'aimedArrivalTime': call['aimedArrivalTime'],
            'expectedArrivalTime': call['expectedArrivalTime']
        }
        s.append(dictio)

    stops_data[name] = s

  return stops_data

if __name__ == "__main__":
    pass