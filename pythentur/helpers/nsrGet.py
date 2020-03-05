import json
import urllib.request

# TODO: Unicode issues

transportation_methods = ['metroStation', 'onstreetBus', 'busStation', 'railStation', 'onstreetTram', 'ferryStop']

# TODO: Some way of viewing the name of the stop place from the ID.
def nsrGet(searchstring, header):
    """Returns list of NSR ID's matching input string.

    searchstring - Searchstring to match up against the National Stop Register database.
    header - Header string in the format 'company - application'
    """
    searchstring = searchstring.replace(" ", "%20")
    url = "https://api.entur.io/geocoder/v1/autocomplete?lang=no&text=" + searchstring
    req = urllib.request.Request(url, headers={'ET-Client-Name': header})
    with urllib.request.urlopen(req) as request:
        json_data = json.loads(request.read().decode())

    features = json_data['features']

    places = []
    for place in features:
        if place['properties']['category'][0] in transportation_methods:
            places.append({
                'id': place['properties']['id'],
                'name': place['properties']['name'],
                'county': place['properties']['county'],
                'locality': place['properties']['locality'],
                'coordinates': place['geometry']['coordinates']
            })

    # TODO: Change print message to actual error.
    if not places:
        print("Could not find any stop places matching that string")
        return None

    return places[0] if len(places) == 1 else places

if __name__ == "__main__":
    pass