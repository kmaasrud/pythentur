API_URL = 'https://api.entur.io/journey-planner/v2/graphql'

GEOCODER_URL = 'https://api.entur.io/geocoder/v1'

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

QUERY_COORDS = """{{
  stopPlace(id: \"{}\") {{
    latitude
    longitude
    tariffZones {{
      id
    }}
  }}
}}"""

QUERY_STOP_PLACE = """{{
  stopPlace(id: \"{}\") {{
      name
      estimatedCalls(timeRange: 72100, numberOfDepartures: {}) {{
        aimedArrivalTime
        expectedArrivalTime
        quay {{
          publicCode
        }}
        destinationDisplay {{
          frontText
        }}
        serviceJourney {{
          journeyPattern {{
            line {{
              publicCode
            }}
          }}
        }}
      }}
    }}
  }}"""

QUERY_JOURNEY = """{{
  trip(
    from: {{
      place: \"{from}\"
    }}
    to: {{
      place: \"{to}\"
    }}
    numTripPatterns: {noDepartures}
    dateTime: \"{time}\"
    minimumTransferTime: 180
  )
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