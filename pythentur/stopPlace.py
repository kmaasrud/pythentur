# Necessary imports
from requests import post
import json
import operator
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import quote

from .helpers import COORDS_QUERY_STOP_PLACE, COORDS_QUERY_PLATFORM, QUERY_CALLS, API_URL, ISO_FORMAT, GEOCODER_URL
from .helpers import prettyTime
from .helpers import decode1252
from .helpers import post_to_api
from . import Location

# ---------------------------------------------------------------------------------------

class StopPlace(Location):
  """Stop place object. Subclass of Location.

  Args:
    stop_place_id (str): The NSR ID of the requested stop place.
    header (str): Header string in the format 'company - application'.
  """

  # If stop place has many platforms, init is a bit slow.
  def __init__(self, stop_place_id, header):
    self._iter = 0
    self.id = stop_place_id
    self.header = header

    data = post_to_api(COORDS_QUERY_STOP_PLACE.format(stop_place_id), self.header)['stopPlace']

    self.zones = [zone['id'] for zone in data['tariffZones']]
    self.platforms = [Platform(quay['id'], header) for quay in data['quays'] if quay['estimatedCalls']]

    super().__init__(data['latitude'], data['longitude'], self.header)

  @classmethod
  def from_string(cls, query, header):
    """Alternative initializer that returns the first stop place matching a query string.

    Args:
      query (str): Search string.
      header (str): Header string in the format 'company - application'.
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
    elif key in [platform.id for platform in self.platforms]:
      return [platform for platform in self.platforms if platform.id == key][0]

    return getattr(self, key)

  def __iter__(self):
    return self

  def __next__(self):
    if self._iter >= len(self):
      self._iter = 0
      raise StopIteration
    platform = self.platforms[self._iter]
    self._iter += 1
    return platform

  def __len__(self):
    return len(self.platforms)

  def __repr__(self):
    return self.id

  def __str__(self):
    return self.name

# ---------------------------------------------------------------------------------------

class Platform(Location):
  """Platform (quay) object. Subclass of Location.

  Args:
    quay_id (str): The NSR ID of the requested platform/quay.
    header (str): Header string in the format 'company - application'.
  """
  def __init__(self, quay_id, header):
    self._iter = 0
    self.id = quay_id
    self.header = header

    data = post_to_api(COORDS_QUERY_PLATFORM.format(self.id), self.header)['quay']

    super().__init__(data['latitude'], data['longitude'], self.header)

    self.transport_modes = set([line['transportMode'] for line in data['lines']])
    self.name = data['publicCode'] # Overrides Location.name
    self.parent = data['stopPlace']['name'] # Name of the parent stop place.
    self.n_calls = 20 # Perhaps not necessary
    self.calls = [None] * self.n_calls # TODO: Method to change this

  def call(self, i):
    """Realtime method to fetch the i-th call from the parent Platform."""
    i = int(i)
    if i >= self.n_calls: return None

    r = post(API_URL,
      json={'query': QUERY_CALLS.format(self.id, i + 1)},
      headers={'ET-Client-Name': self.header}
    )

    try:
      data = json.loads(r.text)['data']['quay']['estimatedCalls'][i]
    except IndexError:
      del self.calls[i:]
      raise IndexError('No more calls available at this moment.')
    else:
      aimed = datetime.strptime(data['aimedArrivalTime'], ISO_FORMAT)
      expected = datetime.strptime(data['expectedArrivalTime'], ISO_FORMAT)
      self.calls[i] = {
        'line': data['serviceJourney']['journeyPattern']['line']['publicCode'],
        'destination': decode1252(data['destinationDisplay']['frontText']),
        'aimed': aimed,
        'expected': expected,
        'delay': expected - aimed,
        'readableTime': prettyTime((expected - datetime.now(timezone.utc)).seconds)
      }
      return self.calls[i]

  def get_all(self):
    """Returns an updated list of all 20 calls from this platform."""
    self.calls = [call for call in self]
    return self.calls

  def __getitem__(self, i):
    return self.call(i)

  def __iter__(self):
    return self

  def __next__(self):
    """Goes to the next call, if it exists and does not have an index greater than n_calls"""
    if self._iter >= self.n_calls:
      self._iter = 0
      raise StopIteration
    try:
      call = self.call(self._iter)
    except IndexError:
      self._iter = 0
      raise StopIteration
    else:
      self._iter += 1
      return call

  def __len__(self):
    self.get_all()
    return len(self.calls)

  def __repr__(self):
    return self.id

  def __str__(self):
    return "{} {}".format(self.parent, self.name)

# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
  pass