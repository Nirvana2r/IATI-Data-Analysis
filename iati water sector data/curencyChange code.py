# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 08:56:50 2022

@author: nirva
"""

from forex_python.converter import CurrencyRates
import datetime as dt
import pandas as pd
import time

c = CurrencyRates()
file = pd.read_csv("df_water_transaction.csv")
#file["Date"] = file["Date"].astype(float)

#date = dt.datetime(file['Date'])
#num = '2019,12,31'

for index, row in file.iterrows():
    #print(row['year'], row['month'])
    date = dt.datetime(row['year'], row['month'], row['day'] ) 
    print(row['default_currency'])
    #print((c.convert(row['default_currency'],'EUR', row['transaction_value'],date)))
    rate = (c.get_rate(row['default_currency'],'EUR', date))
    time.sleep(1)



#print (date.dtypes)

#df_water_transaction['date'] = pd.to_datetime(df_water_transaction['transaction_transaction_date_iso_date'], format='%Y/%m/%d')
#df_water_transaction['date'] = df_water_transaction['transaction_transaction_date_iso_date'].str.replace("-",",").str[:10]
#print(df_water_transaction['date'])

c = CurrencyRates()
#df_water_transaction['EUR'] = df_water_transaction.apply( lambda x: c.convert( x['default_currency'], 'EUR', x['transaction_value'], x['date']), axis = 1)
#df_water_transaction['exchangerate'] = df_water_transaction.apply(c.get_rate(df_water_transaction['default_currency'],'EUR', df_water_transaction['date']))
#df_water_transaction['Rate'] = df_water_transaction.apply(lambda x: c.get_rate(x['default_currency'], 'EUR', x['date']), axis=1)
#print(df_water_transaction.dtypes)