import pandas as pd
import glob

# alpha3Codeをindexに設定して読み込む
country_data = pd.read_csv('../../country.csv', keep_default_na=False, index_col=0)

# 空行を除いて3行目からデータがスタートする（適宜要調整）
# 2列目の「Country Code」をindexに設定する。country.csvと同じ値が入るカラムをindexに指定する必要がある（適宜要調整）
raw_csv = glob.glob('API*.csv')[0]
data = pd.read_csv(raw_csv, header=2, index_col=1)

# country.csvのデータをdataに突合させて挿入していく
# 順番は、「Country Code(世銀カラム),alpha2Code,Country Name(世銀カラム),alias,region,flag_image_url」
data.insert(0, 'alpha2Code', '')
data.insert(2, 'alias', '')
data.insert(3, 'region', '')
data.insert(4, 'flagImageUrl', '')

data = data.assign(
    alpha2Code=country_data.loc[:, 'alpha2Code'],
    alias=country_data.loc[:, 'alias'],
    region=country_data.loc[:, 'region'],
    flagImageUrl='https://www.countryflags.io/' + country_data.loc[:, 'alpha2Code'] + '/flat/64.png'
)

# 「"Arab World","ARB"」のような地域を表現するデータが世銀データには入っているので要注意
# regeonが空白のものがあると、カテゴリ表示にNaNが加わってしまうためregionが空なら削除する
data.dropna(subset=['region'], inplace=True)

# 世銀のデータから削除したい不要なカラム
delete_cols = ['Indicator Name', 'Indicator Code']
data.drop(delete_cols, axis=1, inplace=True)

# 列の値すべてが欠損していたら列を削除する（1960年代ごろから一応カラムは用意されているが、データが入っていない場合がある）
data.dropna(how='all', axis=1, inplace=True)

data.to_csv('data.csv')
