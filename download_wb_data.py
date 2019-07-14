import urllib.request
import xml.etree.ElementTree as ET

# 大きすぎると'Body buffer overflow'を起こす
PER_PAGE = '8500'
url = "https://api.worldbank.org/v2/indicator?per_page=" + PER_PAGE + "&page={}"

page = 1
total_pages = 1  # とりあえず1としておくが、実際にデータを取得してみた結果をもとに、動的に書き換える
while page <= total_pages:

    req = urllib.request.Request(url.format(page))

    xml_resposnse = urllib.request.urlopen(req).read()
    path = "./data/indicator{}.xml"
    with open(path.format(page), mode='wb') as f:
        f.write(xml_resposnse)

    if page == 1:
        root = ET.fromstring(xml_resposnse)
        total_pages = int(root.attrib['pages'])

    page += 1
