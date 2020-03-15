import json
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

from . import Location
from . import Platform
from .helpers import COORDS_QUERY_STOP_PLACE, GEOCODER_URL
from .helpers import post_to_api

class StopPlace(Location):
  """Stop place object. Subclass of Location.

  Args:
    stop_place_id (str): The NSR ID of the requested stop place.
    header (str): Header string in the format 'company - application'.
  """

  def __init__(self, stop_place_id, header):
    self._iter = 0
    self.id = stop_place_id
    self.header = header

    data = post_to_api(COORDS_QUERY_STOP_PLACE.format(stop_place_id), self.header)['stopPlace']

    self.zones = [zone['id'] for zone in data['tariffZones']]

    ids = [quay['id'] for quay in data['quays'] if quay['estimatedCalls']]
    self.platforms = []
    with ThreadPoolExecutor() as executor:
      for result in executor.map(Platform, ids, repeat(self.header)):
        self.platforms.append(result)

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
    if self._iter >= len(self.platforms):
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