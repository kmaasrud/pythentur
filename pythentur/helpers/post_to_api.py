from requests import post
import json

from . import API_URL

def post_to_api(query, header, encode=True):
  r = post(API_URL,
    json={'query': query},
    headers={'ET-Client-Name': header}
  )

  return json.loads(r.text.encode('cp1252').decode('utf-8'))['data']