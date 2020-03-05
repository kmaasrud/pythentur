import json
import urllib.request as urqst
from helpers.constants import GEOCODER_URL

class Location:
    """Doc"""
    def __init__(self, lat, lon, header):
        self.lat = lat
        self.lon = lon
        self.coordinates = [float(lat), float(lon)]

        url = GEOCODER_URL + '/reverse?point.lat={}&point.lon={}&size=1&lang=en'.format(str(lat),str(lon))
        req = urqst.Request(url, headers={'ET-Client-Name': header})
        with urqst.urlopen(req) as request:
            json_data = json.loads(request.read().decode())

        properties = json_data['features'][0]['properties']

        self.name = properties['name']
        self.county = properties['county']
        self.locality = properties['locality']

    @classmethod
    def from_string(cls, query, header):
        query = query.replace(" ", "%20")
        url = GEOCODER_URL + '/autocomplete?text={}&size=1&lang=en'.format(query)
        req = urqst.Request(url, headers={'ET-Client-Name': header})
        with urqst.urlopen(req) as request:
            json_data = json.loads(request.read().decode())

        coords = json_data['features'][0]['geometry']['coordinates']
        return cls(coords[1], coords[0], header)

    def __getitem__(self, key):
        return getattr(self, key)

if __name__ == "__main__":
    pass