import urllib.request
import sys
import zipfile
import os

URL = "http://api.worldbank.org/v2/en/indicator/{}?downloadformat=csv"
ZIP_DOWNLOAD_PATH = "./data/{}.zip"

indicator_id = sys.argv[1]
zip_path = ZIP_DOWNLOAD_PATH.format(indicator_id)

def download():
    urllib.request.urlretrieve(URL.format(indicator_id), zip_path)

if __name__ == "__main__":
    download()

with zipfile.ZipFile(zip_path) as zip:
    zip.extractall('./data/' + indicator_id)

os.remove(zip_path)

# download managerへの登録

import csv
import re
import glob
import json

csv_path = "./data/{}/API*.csv"

paths =  glob.glob(csv_path.format(indicator_id))
print(paths[0])
csv_file = open(paths[0], "r")

f = csv.reader(csv_file)
updated_date = True
for row in f:
    if len(row) > 0:
        if re.match(r".*Updated.*", row[0]):
            updated_date = row[1]
            break

# download_managerに記載
# with open('./indicators_dl_manager.json') as f:
#     df = json.load(f)
#     df[indicator_id] = updated_date
#
#     with open('./indicators_dl_manager.json', mode='w') as f:
#         json.dump(df, f, indent=4)

