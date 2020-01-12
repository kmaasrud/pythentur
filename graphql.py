import requests
import json

def realtime_data(stops):
  """Returns dictionary of realtime transport data from list of Entur stop id's"""

  query_template = """{{
    stopPlace(id: "{}") {{
      name
      estimatedCalls(timeRange: 72100, numberOfDepartures: 10) {{
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
    stops = ['NSR:StopPlace:59516', 'NSR:StopPlace:60245'] # Example list. Stop id's are found at the end of urls from Entur journey planner.
    print(realtime_data(stops))