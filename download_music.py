import urllib.request
import sys
import os
import pandas as pd

duration = int(sys.argv[1])

cur = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv('./audio_library_non_license.csv', header=0)
df_s = df.sample(frac=1)

def calc_second(text):
    texts = text.split(':')
    return int(texts[0]) * 60 + int(texts[1])

raw_duration = duration

while duration >= raw_duration - 5:
    for index, row in df_s.iterrows():
        if duration == calc_second(row[2]):
            req = urllib.request.Request(row[6])

            xml_resposnse = urllib.request.urlopen(req).read()

            os.makedirs("{}/music/{}".format(cur, duration), exist_ok=True)
            path = "{}/music/{}/{}.mp3".format(cur, duration, row[0].replace(' ', '_'))

            with open(path, mode='wb') as f:
                f.write(xml_resposnse)

            print(path)
            break
    else:
        duration =- 1
        continue

    break
