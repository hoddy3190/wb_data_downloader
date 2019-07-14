import urllib.request
import xml.etree.ElementTree as ET
import glob
import collections as cl
import json

indicator_map = cl.defaultdict()

for p in glob.glob("./data/indicator*"):
    print(p)

    tree = ET.parse(p)

    root = tree.getroot()

    for child in root:
        indicator_map[child.attrib['id']] = ''

with open('./indicators_dl_manager.json', mode='w') as f:
    json.dump(indicator_map, f, indent=4)
