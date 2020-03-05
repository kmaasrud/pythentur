# Necessary imports
import requests
import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import quote

from .helpers import QUERY_STOP_PLACE, QUERY_COORDS, API_URL, ISO_FORMAT, GEOCODER_URL
from .helpers import prettyTime
from . import Location

class StopPlace(Location):
  """Stop place object.

  Args:
    nsr_id (str): The NSR ID of the requested stop place.
    header (str): Header string in the format 'company - application'
  """

  def __init__(self, nsr_id, header):
    self.id = nsr_id
    self.header = header
    self.n_departures = 20
    r = requests.post(API_URL, json={'query': QUERY_COORDS.format(nsr_id)}, headers={'ET-Client-Name': self.header})
    self.data = json.loads(r.text.encode('cp1252').decode('utf-8'))['data']['stopPlace']
    self.zones = [zone['id'] for zone in self.data['tariffZones']]
    super().__init__(self.data['latitude'], self.data['longitude'], self.header)

  @classmethod
  def from_string(cls, query, header):
    """Alternative initializer that returns the first stop place matching a query string.

    Args:
      query (str): Search text to
    """
    query = query.replace(" ", "%20")
    url = GEOCODER_URL + '/autocomplete?text={}&size=1&layers=venue&lang=en'.format(quote(query))
    req = Request(url, headers={'ET-Client-Name': header})
    with urlopen(req) as request:
        json_data = json.loads(request.read().decode())

    nsr_id = json_data['features'][0]['properties']['id']

    return cls(nsr_id, header)

  def __repr__(self):
    return "StopPlace('{}', '{}')".format(self.id, self.header)

  def __str__(self):
    return "Stop place: " + self.name

if __name__ == "__main__":
  header = 'kmaasrud - pythentur'
  fyrstikktorget = StopPlace.from_string('fyrstikktorget', header)
  print(fyrstikktorget)


# def get(self):
#   """Retrieves list of dictionaries, containing templated data."""
#   r = requests.post(API_URL, json={'query': self.query}, headers={'ET-Client-Name': self.header})
#   json_data = json.loads(r.text)['data']['stopPlace']

#   now = datetime.now(timezone.utc)
#   data = []
#   for call in json_data['estimatedCalls']:
#     expected = datetime.strptime(call['expectedArrivalTime'], ISO_FORMAT)
#     aimed = datetime.strptime(call['aimedArrivalTime'], ISO_FORMAT)
#     data.append({
#         'platform': call['quay']['publicCode'],
#         'line': call['serviceJourney']['journeyPattern']['line']['publicCode']+" "+call['destinationDisplay']['frontText'],
#         'aimedArrivalTime': aimed,
#         'expectedArrivalTime': expected,
#         'delay': expected - aimed,
#         'readableTime': prettyTime((expected - now).seconds)
#     })