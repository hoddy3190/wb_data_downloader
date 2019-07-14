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
