import pandas as pd
import json
import collections as cl
import numpy

# alpha3Codeをindexに設定して読み込む
csv = pd.read_csv('./data.csv', header=0, index_col=1)
columns = csv.columns

# columns.data.valuesの中身を取得
# 必ずflagImageUrlの横からyearが始まる
years = []
years_index = []
image_url_col_index = columns.size
for i in range(columns.size):
    if columns[i] == "flagImageUrl":
        image_url_col_index = i
    if i > image_url_col_index:
        years.append(columns[i])
        years_index.append(i)


'''
{
                "category": "Central America",
                "image": "https://www.countryflags.io/AW/flat/64.png",
                "label": "Aruba",
                "values": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2.86831939212055", "7.235198033412581", "10.0261792105306", "10.6347325992922", "26.3745032100275", "26.0461298009966", "21.4425588041328", "22.000786163522", "21.036245110821397", "20.7719361585578", "20.318353365384603", "20.4268177083943", "20.587669145364803", "20.311566765912", "26.194875238021897", "25.9340244138733", "25.671161782044802", "26.420452085716896", "26.5172934158421", "27.200707780588", "26.9477259654482", "27.895022821125803", "26.229552674677898", "25.915322063969196", "24.670528873107802", "24.507516218176104", "13.157722308892401", "8.35356100776471", "8.41006417792511"]
            }
'''

# data.dataの取得
data = []

for index, row in csv.iterrows():
    hash = cl.OrderedDict()

    hash['category'] = row['region'] if isinstance(row['region'], str) else ''
    hash['image'] = row['flagImageUrl'] if isinstance(row['flagImageUrl'], str) else ''
    hash['label'] = row['alias'] if isinstance(row['alias'], str) else ''

    hash['values'] = []

    for i in years_index:
        if numpy.isnan(row[i]):
            row[i] = 0
        hash['values'].append(row[i])

    data.append(hash)



json_hash = cl.OrderedDict()

json_hash['settings'] = cl.OrderedDict()

json_hash['columns'] = cl.OrderedDict()
json_hash['columns']['data'] = cl.OrderedDict()
json_hash['columns']['data']['values'] = years

json_hash['data'] = cl.OrderedDict()
json_hash['data']['data'] = data


fw = open('data.json','w')
json.dump(json_hash, fw, indent=4)
