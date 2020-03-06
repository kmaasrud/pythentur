# Necessary imports
import requests
import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import quote

from .helpers import COORDS_QUERY_STOP_PLACE, COORDS_QUERY_PLATFORM, QUERY_CALLS, API_URL, ISO_FORMAT, GEOCODER_URL
from .helpers import prettyTime
from . import Location

# ---------------------------------------------------------------------------------------

class StopPlace(Location):
  """Stop place object.

  Args:
    stop_place_id (str): The NSR ID of the requested stop place.
    header (str): Header string in the format 'company - application'
  """

  # If stop place has many platforms, init is a bit slow.
  def __init__(self, stop_place_id, header):
    self.id = stop_place_id
    self.header = header
    self.n_departures = 20

    r = requests.post(API_URL,
      json={'query': COORDS_QUERY_STOP_PLACE.format(stop_place_id)},
      headers={'ET-Client-Name': header}
    )

    self.data = json.loads(r.text.encode('cp1252').decode('utf-8'))['data']['stopPlace']
    self.zones = [zone['id'] for zone in self.data['tariffZones']]
    self.platforms = [Platform(quay['id'], header) for quay in self.data['quays']]

    super().__init__(self.data['latitude'], self.data['longitude'], self.header)

  @classmethod
  def from_string(cls, query, header):
    """Alternative initializer that returns the first stop place matching a query string.

    Args:
      query (str): Search string.
      header (str): Header string in the format 'company - application'
    """
    url = GEOCODER_URL + '/autocomplete?text={}&size=1&layers=venue&lang=en'.format(quote(query))
    req = Request(url, headers={'ET-Client-Name': header})
    with urlopen(req) as request:
        json_data = json.loads(request.read().decode())

    stop_place_id = json_data['features'][0]['properties']['id']

    return cls(stop_place_id, header)

  def __getitem__(self, key):
    if key in [platform.name for platform in self.platforms]:
      return [platform for platform in self.platforms if platform.name == key][0]

    return getattr(self, key)

  def __len__(self):
    return len(self.platforms)

  def __repr__(self):
    return self.id

  def __str__(self):
    return "Stop place: " + self.name

# ---------------------------------------------------------------------------------------

class Platform(Location):
  """Doc"""
  def __init__(self, quay_id, header):
    self.id = quay_id
    self.header = header

    r = requests.post(API_URL,
      json={'query': COORDS_QUERY_PLATFORM.format(quay_id)},
      headers={'ET-Client-Name': header}
    )

    data = json.loads(r.text.encode('cp1252').decode('utf-8'))['data']['quay']
    super().__init__(data['latitude'], data['longitude'], self.header)
    self.transport_modes = set([line['transportMode'] for line in data['lines']])
    self.name = data['publicCode'] # Overrides Location.name
    self.n_calls = 20 # Perhaps not necessary
    self.calls = [0] * self.n_calls # TODO: Method to change this

  def call(self, i):
    i = int(i)
    now = datetime.now(timezone.utc)

    r = requests.post(API_URL,
      json={'query': QUERY_CALLS.format(self.id, i + 1)},
      headers={'ET-Client-Name': self.header}
    )

    data = json.loads(r.text.encode('cp1252').decode('utf-8'))['data']['quay']['estimatedCalls'][i]
    aimed = datetime.strptime(data['aimedArrivalTime'], ISO_FORMAT)
    expected = datetime.strptime(data['expectedArrivalTime'], ISO_FORMAT)
    self[i] = {
      'aimed': aimed,
      'expected': expected,
      'line': data['serviceJourney']['journeyPattern']['line']['publicCode'],
      'destination': data['destinationDisplay']['frontText'],
      'delay': expected - aimed,
      'readableTime': prettyTime((expected - now).seconds)
    }

  def __setitem__(self, i, value):
    self.calls[int(i)] = value

  def __getitem__(self, i):
    self.call(i)
    return self.calls[i]

  def __repr__(self):
    return self.id

  def __str__(self):
    return "Platform " + self.name

# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
  pass


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