#!/usr/bin/env python3

import tabula
import re
import datetime

file = '1_06_NZANR_Part_71_Visual_Reporting_Points_VRP.pdf'

def parse_lat_lon( anr_str ):
  matches = re.fullmatch( '^(\d*?)(\d{2})(\d{2})\.(\d+)([NSEW])$', anr_str )
  if matches:

    multiplier = 1
    if ( matches[5] == 'S' ) or ( matches[5] == 'W' ):
      multiplier = -1

    return {
      'degrees': matches[1],
      'minutes': matches[2],
      'seconds': f'{matches[3]}.{matches[4]}',
      'cardinal': matches[5],
      'decimal': str(
        round(
          (
            int( matches[1] ) +
            int( matches[2] ) / 60 +
            int( matches[3] ) / 3600 + float( f'0.{matches[4]}' ) / 3600
          ) * multiplier
        , 6 )
      )
    }
  return False

# Read data from tables.
tables = tabula.read_pdf( file, pages='all', output_format='json' )

# Time that we read the file.
now = datetime.datetime.now(datetime.timezone.utc)
created = now.strftime( '%Y-%m-%dT%H:%M:%SZ' )

# Parse the data and create array with results.
vrps = []
for page in tables:
  for row in page['data']:
    lat = parse_lat_lon( row[1]['text'] )
    lon = parse_lat_lon( row[2]['text'] )

    # Skip header rows
    if ( not lat ) or ( not lon ):
      continue
    vrps.append({
      'name': row[0]['text'].title(),
      'lat':  lat['decimal'],
      'lon':  lon['decimal'],
    })


# This is very simple XML, so we'll just print it ourselves.
print( '<?xml version="1.0" encoding="UTF-8"?>' )
print( '<flight-plan xmlns="http://www8.garmin.com/xmlschemas/FlightPlan/v1">' )
print( f'<created>{created}</created>' )
print( '<waypoint-table>' )

# This is horribly unpythonic, but it works.
for vrp in vrps:
  print( '    <waypoint>' )
  print( f"        <identifier>{vrp['name']}</identifier>" )
  print( '        <type>USER WAYPOINT</type>' )
  print( '        <country-code>NZ</country-code>' )
  print( f"        <lat>{vrp['lat']}</lat>" )
  print( f"        <lon>{vrp['lon']}</lon>" )
  print( '        <comment></comment>' )
  print( '    </waypoint>' )

print( '</waypoint-table>' )
