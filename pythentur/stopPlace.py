# Necessary imports
import requests
import json
from datetime import datetime, timezone
from .prettyTime import prettyTime
from .constants import QUERY_STOP_PLACE, API_URL, ISO_FORMAT

class StopPlace():
  """Stop place object.

  Args:
    nsr_id (str): The NSR ID of the requested stop place.
    header (str): Header string in the format 'company - application'

  Keyword args:  
    noDepatures (int): Specifies entries to retrieve. Default is 20.
  """
  def __init__(self, nsr_id, header, noDepartures = 20):
    self.id = nsr_id
    self.query = QUERY_STOP_PLACE.format(self.id, noDepartures)
    r = requests.post(API_URL, json={'query': self.query}, headers={'ET-Client-Name': 'kmaasrud - pythentur'}) # TODO: Not all requests should go through me. Require custom header.
    json_data = json.loads(r.text)['data']['stopPlace']
    self.name = json_data['name']
    self.header = header

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

  def __setitem__(self, key, value)

  def __getitem__(self, key):
    pass

  def __repr__(self):
    pass

  def __str__(self):
    pass

if __name__ == "__main__":
  pass