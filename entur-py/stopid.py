import json
import urllib.request
import sys

def stopid(searchstring):
    """Returns list of NSR ID's matching input string."""
    searchstring = searchstring.replace(" ", "%20")
    url = "https://api.entur.io/geocoder/v1/autocomplete?lang=no&text=\""+searchstring+"\""
    with urllib.request.urlopen(url) as request:
        json_data = json.loads(request.read().decode())

    features = json_data['features']

    places = []
    for place in features:
        if place['properties']['category'][0] in ['metroStation', 'onstreetBus', 'busStation', 'railStation']:
            places.append(place['properties']['id'])

    return places

if __name__ == "__main__":
    args = sys.argv
    for i in range(1,len(args)):
        print(args[i] + ": " + str(stopid(args[i])))