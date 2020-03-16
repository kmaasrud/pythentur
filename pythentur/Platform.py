from requests import post
import json
from datetime import datetime, timezone

from . import Location
from .helpers import COORDS_QUERY_PLATFORM, API_URL, QUERY_CALLS, ISO_FORMAT
from .helpers import post_to_api, decode1252, prettyTime

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