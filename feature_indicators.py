import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = 'https://data.worldbank.org/indicator?tab=featured'

r = requests.get(BASE_URL)
soup = BeautifulSoup(r.content, "html.parser")

feature_indicators = []
for link in soup.findAll('a'):
    if link.get('href'):
        m = re.match(r"\/indicator\/(.*)\?view=chart", link.get('href'))
        if m:
            feature_indicators.append(m.group(1))

with open('./feature_indicators.json', mode='w') as f:
    json.dump(feature_indicators, f, indent=4)
