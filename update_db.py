import sqlite3
import pandas as pd
import requests
import os
import csv
import json
#import config


#Fear and Greed index in 1D timeframe
CSV_URL = 'https://api.alternative.me/fng/?limit=0&format=csv'


with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    my_list = my_list[4:-5]

        
df = pd.DataFrame(my_list,columns = ['date','fng_value','fng_class'])
df['date'] = pd.to_datetime(df['date'],format = '%d-%m-%Y')


#BTC price data in 1D timeframe
btc = 'https://api.cryptowat.ch/markets/binance/btcusdt/ohlc?periods=86400'
with requests.Session() as s:
    download = s.get(btc)

    decoded_content = download.content.decode('utf-8')
    
jn = json.loads(decoded_content)
price = pd.DataFrame(jn['result']['86400'], columns = ['date','Open','High', 'Low', 'Close', 'Volume_btc','Volume_usd'])
price['date'] = pd.to_datetime(price['date'],unit = 's')    


#SOPR value in 1D timeframe
onc = requests.get('https://api.cryptoquant.com/v1/Bitcoin/Exchange-Flows')
#API_KEY = config.api_key
API_KEY = os.environ['API_KEY_GLASSNODE']
print(API_KEY)

res = requests.get('https://api.glassnode.com/v1/metrics/indicators/sopr',
    params={'a': 'BTC', 'api_key': API_KEY})

rs = res.content.decode('utf-8')

# convert to pandas dataframe
sopr = pd.read_json(res.text, convert_dates=['t'])
sopr.rename(columns={'t':'date', 'v':'sopr_val'}, inplace = True)


# Join the three tables on date into a single dataframe

pfng = df.merge(price, on = 'date', how='inner')
pfngs = pfng.merge(sopr, on = 'date', how='inner')
pfngs = pfngs[::-1].reset_index(drop = True)
#pfngs.to_csv(r'btc_pfngs.csv', index=False)
pfngs.set_index('date', inplace=True)

# Drop fear-Greed categorical variable as fear and greed value is retained
pfngs.drop(columns='fng_class', inplace=True)

conn = sqlite3.connect("btc.db")
cursor = conn.cursor()

pfngs.to_sql('btcprice',conn,if_exists="replace")

conn.close()
