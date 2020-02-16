import requests
import json
import sys
from datetime import datetime

class Journey():
    def __init__(self):
        pass

# TODO: Preferred or banned transport modes.
query_template = """{{
  trip(
    from: {{
      place: {from}
    }}
    to: {{
      place: {to}
    }}
    numTripPatterns: 5
    dateTime: {time}
    minimumTransferTime: 180
  )

#### Requested fields
  {{
    tripPatterns {{
      duration
      legs {{
        mode
        aimedStartTime
        expectedStartTime
        fromEstimatedCall {{
          destinationDisplay {{
            frontText
          }}
        }}
        line {{
          publicCode
          name
          presentation {{
            colour
          }}
        }}
        fromPlace{{
          quay {{
            stopPlace {{
              name
              id
            }}
          }}
        }}
        toPlace {{
          quay {{
            stopPlace {{
              name
              id
            }}
          }}
        }}
      }}
    }}
  }}
}}"""

api_url = 'https://api.entur.io/journey-planner/v2/graphql'

iso_datestring = "%Y-%m-%dT%H:%M:%S%z"