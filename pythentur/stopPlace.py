# Necessary imports
import requests
import json
from datetime import datetime, timezone
import urllib.request as urqst

from helpers.prettyTime import prettyTime
from helpers.constants import QUERY_STOP_PLACE, QUERY_COORDS, API_URL, ISO_FORMAT, GEOCODER_URL
from Location import Location

class StopPlace(Location):
  """Stop place object.

  Args:
    nsr_id (str): The NSR ID of the requested stop place.
    header (str): Header string in the format 'company - application'

  Keyword args:  
    noDepatures (int): Specifies entries to retrieve. Default is 20.
  """

  def __init__(self, nsr_id, header):
    self.id = nsr_id
    self.header = header
    self.n_departures = 20
    r = requests.post(API_URL, json={'query': QUERY_COORDS.format(nsr_id)}, headers={'ET-Client-Name': self.header})
    coords = json.loads(r.text)['data']['stopPlace']
    super().__init__(coords['latitude'], coords['longitude'], self.header)

  @classmethod
  def from_string(cls, query, header):
    query = query.replace(" ", "%20")
    url = GEOCODER_URL + '/autocomplete?text={}&size=1&layers=venue&lang=en'.format(query)
    req = urqst.Request(url, headers={'ET-Client-Name': header})
    with urqst.urlopen(req) as request:
        json_data = json.loads(request.read().decode())

    nsr_id = json_data['features'][0]['properties']['id']

    return cls(nsr_id, header)

  def get(self):
    """Retrieves list of dictionaries, containing templated data."""
    r = requests.post(API_URL, json={'query': self.query}, headers={'ET-Client-Name': self.header})
    json_data = json.loads(r.text)['data']['stopPlace']

    now = datetime.now(timezone.utc)
    data = []
    for call in json_data['estimatedCalls']:
      expected = datetime.strptime(call['expectedArrivalTime'], ISO_FORMAT)
      aimed = datetime.strptime(call['aimedArrivalTime'], ISO_FORMAT)
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

  def __repr__(self):
    pass

  def __str__(self):
    pass

if __name__ == "__main__":
  header = 'kmaasrud - pythentur'
  fyrstikktorget = StopPlace.from_string('fyrstikktorget', header)
  print(fyrstikktorget['id'])