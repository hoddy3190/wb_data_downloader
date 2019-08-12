import xml.etree.ElementTree as ET
import glob
import collections as cl
import json
import os
import pandas as pd
from keyword_extract import TextRank4Keyword

indicator_id = os.getcwd().split('/')[-1]


# alpha3Codeをindexに設定して読み込む
csv = pd.read_csv('./data.csv', header=0, index_col=1)
columns = csv.columns

# columns.data.valuesの中身を取得
# 必ずflagImageUrlの横からyearが始まる
years = []
image_url_col_index = columns.size
for i in range(columns.size):
    if columns[i] == "flagImageUrl":
        image_url_col_index = i
    if i > image_url_col_index:
        years.append(columns[i])

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
json_hash['language'] = 'en'

title_str = "TOP 10 {} ({} - {})"

for p in glob.glob("../indicator*"):

    tree = ET.parse(p)
    root = tree.getroot()

    for child in root:
        if child.attrib['id'] == indicator_id:
            for e in child:
                if e.tag == '{http://www.worldbank.org}name':
                    json_hash['title'] = title_str.format(e.text, years[0], years[-1])
                if e.tag == '{http://www.worldbank.org}sourceNote':
                    json_hash['description'] = e.text
            break


tr4w = TextRank4Keyword()
tr4w.analyze(json_hash['title'] + json_hash['description'], candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
keywords = tr4w.get_keywords_arr(3)

default_tags = ['ranking', 'world', 'education', 'graph', 'country']


json_hash['tags'] = []
for tag in default_tags + keywords:
    if tag not in json_hash['tags']:
        json_hash['tags'].append(tag)


hash_tags_list = list(map(lambda x: '#' + x, json_hash['tags']))
hash_tags_list_str = "\n\n" + ' '.join(hash_tags_list)

json_hash['description'] += "\n\nData Souce\n  - The World Bank\nLICENSE\n  - https://datacatalog.worldbank.org/public-licenses#cc-by"
json_hash['description'] += hash_tags_list_str

fw = open('meta_data.json','w')
json.dump(json_hash, fw, indent=4)
