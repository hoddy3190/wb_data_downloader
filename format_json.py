import pandas as pd
import json
import collections as cl
import numpy
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

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

# 値をまるめる

max = csv[years[-1]].max()
max_keta = len(str(math.floor(max)))

unit = 0
keta = 0
while max_keta - unit > 7 and unit <= 9:
    if max_keta - unit <= 7:
        keta = max_keta - unit
        break
    unit += 3

# 2,487,045,000,000 13桁
# 有効数字5桁 - 7桁になるように調整する

# 12 - 9 = 3
# 12 - 6 = 6
#
# 13 - 9 = 4
# 13 - 6 = 7
#
# 14 - 9 = 5
# 14 - 6 = 8
#
# 15 - 9 = 6
# 15 - 6 = 9

def val_round(val, units):
    if val == float(math.ceil(val)):
        val = math.ceil(val)
    if units == 0:
        return val
    val = val / (10 ** units)
    if val == float(math.ceil(val)):
        val = math.ceil(val)
    return(float(Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))


# data.dataの取得
data = []
zero_rate_list = []
for index, row in csv.iterrows():
    hash = cl.OrderedDict()

    hash['category'] = row['region'] if isinstance(row['region'], str) else ''
    hash['image'] = row['flagImageUrl'] if isinstance(row['flagImageUrl'], str) else ''
    hash['label'] = row['alias'] if isinstance(row['alias'], str) else ''

    hash['values'] = []

    first_valid_val_index = 0
    zero_count = 0

    for i in years_index:
        if numpy.isnan(row[i]):
            row[i] = ''
            if not first_valid_val_index == 0:
                zero_count += 1
            hash['values'].append('')
        else:
            if first_valid_val_index == 0:
                first_valid_val_index = i
            hash['values'].append(val_round(row[i], unit)) # 値を挿入

    if first_valid_val_index == 0:
        zero_rate = 1
    else:
        zero_rate = zero_count / (years_index[-1] - first_valid_val_index + 1)

    zero_rate_list.append(zero_rate)

    data.append(hash)


zero_rate_ave = sum(zero_rate_list) / len(zero_rate_list)

# settingsの取得

json_hash = cl.OrderedDict()

json_hash['settings'] = cl.OrderedDict()
with open('./meta_data.json') as f:
    df = json.load(f)
    json_hash['settings']['layout.title'] = df['title']

layout_text = ''
if unit == 3:
    layout_text = 'unit: thousand'
elif unit == 6:
    layout_text = 'unit: million'
elif unit == 9:
    layout_text = 'unit: billion'

json_hash['settings']['layout.text'] = layout_text

if zero_rate_ave > 0.2:
    json_hash['settings']['blank_cells'] = 'last_valid'

# columns

json_hash['columns'] = cl.OrderedDict()
json_hash['columns']['data'] = cl.OrderedDict()
json_hash['columns']['data']['values'] = years

# data

json_hash['data'] = cl.OrderedDict()
json_hash['data']['data'] = data


fw = open('data.json','w')
json.dump(json_hash, fw, indent=4)
