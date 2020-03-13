API_URL = 'https://api.entur.io/journey-planner/v2/graphql'

GEOCODER_URL = 'https://api.entur.io/geocoder/v1'

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

COORDS_QUERY_STOP_PLACE = """{{
  stopPlace(id: \"{}\") {{
    latitude
    longitude
    tariffZones {{
      id
    }}
    quays {{
      id
      estimatedCalls(numberOfDepartures: 1) {{
        date
      }}
    }}
  }}
}}"""

COORDS_QUERY_PLATFORM = """{{
  quay(id: \"{}\") {{
    latitude
    longitude
    publicCode
    lines {{
      transportMode
    }}
    stopPlace {{
      name
    }}
  }}
}}"""

QUERY_CALLS = """{{
  quay(id: \"{}\") {{
      estimatedCalls(timeRange: 72100, numberOfDepartures: {}) {{
        aimedArrivalTime
        expectedArrivalTime
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
          presentation {{
            colour
          }}
        }}
        fromPlace{{
          quay {{
            publicCode
            stopPlace {{
              name
              id
            }}
          }}
        }}
        toPlace {{
          quay {{
            publicCode
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