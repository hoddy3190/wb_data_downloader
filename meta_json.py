import xml.etree.ElementTree as ET
import glob
import collections as cl
import json
import os

indicator_id = os.getcwd().split('/')[-1]


json_hash = cl.OrderedDict()

"""
{
  "title": "my test title",
  "description": "my test description",
  "tags": ["test tag1", "test tag2"],
  "privacyStatus": "private",
  "embeddable": true,
  "license": "creativeCommon",
  "publicStatsViewable": true,
  "publishAt": "2017-06-01T12:05:00+02:00",
  "categoryId": "10",
  "recordingdate": "2017-05-21",
  "location": {
    "latitude": 48.8584,
    "longitude": 2.2945
  },
  "locationDescription":  "Eiffel Tower",
  "playlistIds":  ["xxxxxxxxxxxxxxxxxx", "yyyyyyyyyyyyyyyyyy"],
  "playlistTitles":  ["my test playlist"],
  "language":  "fr"
}
"""

json_hash['license'] = 'creativeCommon'
json_hash['tags'] = ['education', 'graph', 'country', 'world']
json_hash['language'] = 'en'

for p in glob.glob("../indicator*"):

    tree = ET.parse(p)
    root = tree.getroot()

    for child in root:
        if child.attrib['id'] == indicator_id:
            for e in child:
                if e.tag == '{http://www.worldbank.org}name':
                    json_hash['title'] = e.text
                if e.tag == '{http://www.worldbank.org}sourceNote':
                    json_hash['description'] = e.text + '\n\nData Souce\n  - The World Bank\nLICENSE\n  - https://datacatalog.worldbank.org/public-licenses#cc-by'
            break

fw = open('meta_data.json','w')
json.dump(json_hash, fw, indent=4)
