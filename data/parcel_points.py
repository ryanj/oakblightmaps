
#
# Computes are rough center point for each parcel feature
#

import json
import re

feature_pat = re.compile('"type":\\s*"Feature"')

header = """{
"type": "FeatureCollection",
"features": [ """

footer = """]
}"""

def parcel_apn(p):
    return p['properties']['APN']

def parcel_coords(p):
    return p['geometry']['coordinates'][0]

def parcel_middle(p):
    coords = parcel_coords(p)
    max_lat = max([ll[0] for ll in coords])
    max_lon = max([ll[1] for ll in coords])
    min_lat = min([ll[0] for ll in coords])
    min_lon = min([ll[1] for ll in coords])

    return min_lat + ((max_lat - min_lat) / 2), min_lon + ((max_lon - min_lon) / 2)

def make_feature(apn, mid):
    d = {}
    d['type'] = 'Feature'
    d['properties'] = { 'APN': apn }
    d['geometry'] = { 'type': 'Point', 'coordinates': mid }
    return d

print header

with open('parcels.json', 'r') as f:
    for line in f:
        if feature_pat.search(line):
            f0 = json.loads(line)
            print json.dumps(make_feature(parcel_apn(f0), parcel_middle(f0))), ","

print footer
