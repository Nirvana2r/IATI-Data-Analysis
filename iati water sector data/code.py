# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 04:15:05 2022

@author: nirva
"""

import pandas as pd
from forex_python.converter import CurrencyRates

#########################  Importing data from water sector ########################################

df1 = pd.read_csv('Niger_iatidata_14010_transaction.csv')
df2 = pd.read_csv('Niger_iatidata_14015_transaction.csv')
df3 = pd.read_csv('Niger_iatidata_14020_transaction.csv')
df4 = pd.read_csv('Niger_iatidata_14021_transaction.csv')
df5 = pd.read_csv('Niger_iatidata_14022_transaction.csv')
df6 = pd.read_csv('Niger_iatidata_14030_transaction.csv')
df7 = pd.read_csv('Niger_iatidata_14031_transaction.csv')
df8 = pd.read_csv('Niger_iatidata_14032_transaction.csv')
df9 = pd.read_csv('Niger_iatidata_14040_transaction.csv')
df10 = pd.read_csv('Niger_iatidata_14050_transaction.csv')
df11 = pd.read_csv('Niger_iatidata_14081_transaction.csv')

######################################################################################################
df1['sector_code'] = df1['sector_code'].map('14010'.format)
df2['sector_code'] = df2['sector_code'].map('14015'.format)
df3['sector_code'] = df3['sector_code'].map('14020'.format)
df4['sector_code'] = df4['sector_code'].map('14021'.format)
df5['sector_code'] = df5['sector_code'].map('14022'.format)
df6['sector_code'] = df6['sector_code'].map('14030'.format)
df7['sector_code'] = df7['sector_code'].map('14031'.format)
df8['sector_code'] = df8['sector_code'].map('14032'.format)
df9['sector_code'] = df9['sector_code'].map('14040'.format)
df10['sector_code'] = df10['sector_code'].map('14050'.format)
df11['sector_code'] = df11['sector_code'].map('14081'.format)


df1['sector'] = df1['sector_code'].map(
    'Water sector policy and administrative management'.format)
df2['sector'] = df2['sector_code'].map(
    'Water resources conservation (including data collection)'.format)
df3['sector'] = df3['sector_code'].map(
    'Water supply and sanitation - large systems'.format)
df4['sector'] = df4['sector_code'].map('Water supply - large systems'.format)
df5['sector'] = df5['sector_code'].map('Sanitation - large systems'.format)
df6['sector'] = df6['sector_code'].map(
    'Basic drinking water supply and basic sanitation'.format)
df7['sector'] = df7['sector_code'].map('Basic drinking water supply'.format)
df8['sector'] = df8['sector_code'].map('Basic sanitation'.format)
df9['sector'] = df9['sector_code'].map('River basins development'.format)
df10['sector'] = df10['sector_code'].map('Waste management/disposal'.format)
df11['sector'] = df11['sector_code'].map(
    'Education and training in water supply and sanitation'.format)


frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11]

df = pd.concat(frames)

df_water = df[['dataset_generated_datetime', 'last_updated_datetime', 'default_currency', 'iati_identifier', 'reporting_org_narrative', 'title_narrative', 'description_type', 'description_narrative', 'participating_org_role', 'participating_org_narrative', 'activity_date_type', 'activity_date_iso_date', 'contact_info_organisation_narrative', 'contact_info_department_narrative', 'recipient_country_code', 'location_name_narrative', 'location_activity_description_narrative', 'sector_code', 'sector_narrative',
               'transaction_transaction_type_code', 'planned_disbursement_period_start_iso_date', 'planned_disbursement_period_end_iso_date', 'planned_disbursement_value', 'planned_disbursement_value_currency', 'planned_disbursement_value_value_date', 'transaction_transaction_date_iso_date', 'transaction_value', 'transaction_value_value_date', 'transaction_description_narrative', 'transaction_provider_org_ref', 'transaction_provider_org_narrative', 'document_link_url', 'conditions_condition_narrative', 'sector']]


################ transactions #############################
df_water_transaction = df[['iati_identifier', 'reporting_org_narrative', 'title_narrative', 'description_narrative',
                           'participating_org_narrative', 'contact_info_organisation_narrative','recipient_country_code',
                           'sector_code', 'sector','sector_narrative', 'transaction_transaction_type_code',
                           'transaction_transaction_date_iso_date', 'transaction_value', 'default_currency',
                           'transaction_description_narrative', 'transaction_provider_org_ref', 'transaction_provider_org_narrative']]
df_water_transaction.reset_index(drop=True, inplace=True)


# only disbursments
#df_water_transaction = df_water_transaction[df_water_transaction['transaction_description_narrative'].str.contains("burs")==True]
df_water_transaction = df_water_transaction[df_water_transaction['transaction_transaction_type_code'].isin([
                                                                                                           2, 3])]

# take only the dates
df_water_transaction['year'] = pd.DatetimeIndex(
    df_water_transaction['transaction_transaction_date_iso_date']).year
df_water_transaction['month'] = pd.DatetimeIndex(
    df_water_transaction['transaction_transaction_date_iso_date']).month
df_water_transaction['day'] = pd.DatetimeIndex(
    df_water_transaction['transaction_transaction_date_iso_date']).day

# convert data types
df_water_transaction['transaction_value'] = df_water_transaction['transaction_value'].astype(
    'int64')

################### exchange Currency : to today's rate value  ##################

exchange_Rate = pd.read_excel("Exchange_Rate_Report.xlsx")
exchange_Rate = exchange_Rate.rename(columns={'Euro   (EUR)                     ': 'EUR',
                                              'U.S. dollar   (USD)                     ': 'USD',
                                              'Australian dollar   (AUD)                     ': 'AUD',
                                              'Canadian dollar   (CAD)                     ': 'CAD',
                                              'Swiss franc   (CHF)                     ': 'CHF',
                                              'Danish krone   (DKK)                     ': 'DKK',
                                              'U.K. pound   (GBP)                     ': 'GBP',
                                              'Japanese yen   (JPY)                     ': 'JPY'})

# ISO 4217 currency code for special drawing rights is XDR, they are often referred to by their acronym SDR
#Unit FMI DTS - XDR
exchange_Rate['XDR'] = 1
exchange_Rate = exchange_Rate[['Date', 'EUR', 'USD','AUD', 'CAD', 'CHF', 'DKK', 'GBP', 'XDR', 'JPY']]


# print(exchange_Rate.info())
df_water_transaction = df_water_transaction.rename(
    columns={'transaction_transaction_date_iso_date': 'Date'})

df_water_transaction['Date'] = pd.to_datetime(
    df_water_transaction['Date'], utc=True)
exchange_Rate['Date'] = pd.to_datetime(exchange_Rate['Date'], utc=True)

# print(exchange_Rate.dtypes)
# print(df_water_transaction['Date'].dtypes)
df_exchange = pd.merge(df_water_transaction,
                       exchange_Rate, on='Date', how='left')


# change nan values to it's curency
df_exchange['default_currency'] = df_exchange['default_currency'].astype(
    "string")
df_exchange['default_currency'] = df_exchange['default_currency'].fillna(
    df_exchange['participating_org_narrative'])
df_exchange['default_currency'] = df_exchange['default_currency'].replace(
    {'EU,MINISTERIO DE AGRICULTURA DE NÍGER,TRAGSA,MINISTERIO DE AGRICULTURA DE NÍGER': 'EUR', 'Recipient Government,Japan,Japan International Cooperation Agency,Recipient Government': 'JPY'}).astype("string")

# fill nan value with average rate of curency
#df_exchange['XDR'] = df_exchange['XDR'].fillna(exchange_Rate['XDR'].mean()).astype("float")
df_exchange[['EUR', 'USD','AUD', 'CAD', 'CHF', 'DKK', 'GBP', 'XDR', 'JPY']] = df_exchange[['EUR', 'USD','AUD', 'CAD', 'CHF', 'DKK', 'GBP', 'XDR', 'JPY']].fillna(
    df_exchange[['EUR', 'USD','AUD', 'CAD', 'CHF', 'DKK', 'GBP', 'XDR', 'JPY']].mean()).astype("float")

#df_exchange.reset_index(drop=True, inplace=True)
#df_exchange = df_exchange.sort_values(by=['default_currency'], ascending=[True])

##### groupe rate per year per currency

grouped_rate = df_exchange.groupby(['default_currency', 'year']).agg({'EUR': ['mean'],'USD': ['mean'],'AUD': ['mean'], 'CAD': ['mean'], 'CHF': ['mean'], 'DKK': ['mean'], 'GBP': ['mean'], 'XDR': ['mean'], 'JPY': ['mean']})
#  columns
grouped_rate.columns = ['EUR', 'USD','AUD', 'CAD', 'CHF', 'DKK', 'GBP', 'XDR', 'JPY']
grouped_rate = grouped_rate.reset_index()
grouped_rate = grouped_rate[grouped_rate['year'].isin([2021, 2020, 2019, 2018, 2017]) ]
grouped_rate.reset_index(drop=True, inplace=True)

############# convert in today's EUR rate for each currency 04/08/2022 #####################
grouped_rate['USD'] = grouped_rate['USD']*0.97718
grouped_rate['AUD'] = grouped_rate['AUD']*0.68051
grouped_rate['CAD'] = grouped_rate['CAD']*0.75899
grouped_rate['CHF'] = grouped_rate['CHF']*1.02227
grouped_rate['DKK'] = grouped_rate['DKK']*0.13438
grouped_rate['GBP'] = grouped_rate['GBP']*1.18656
grouped_rate['XDR'] = grouped_rate['XDR']*1.29463 
grouped_rate['JPY'] = grouped_rate['JPY']*0.0073362
#df_exchange.to_csv("df_exchange.csv")
'''
##### exchange rate test code
df_exchange['a'] = df_exchange[df_exchange['default_currency'].str.contains('USD')]
#df_exchange['a'] = df_exchange['transaction_value']*df_exchange['USD']


for index in range(len(df_exchange)):
    #df_exchange['a'] =(df_exchange['EUR'][index])
    df_exchange['a'] = (df_exchange['EUR'][index])
#for index, row in df_exchange.iterrows():
    if row['default_currency'] == 'USD':
        df_exchange['a'] = row['EUR']*1
    else:
       df_exchange['a'] = row['transaction_value']*0
        
#for i in range(len(df_exchange)):
    
    #df2 = df_exchange[[row['transaction_value']]]

    #df_exchange['a'] = [col for col in df_exchange.columns if row['default_currency'] in col]
    #df_exchange['a'] = (row['transaction_value'] * row['year']).where(df_exchange['default_currency'] == [col for col in df_exchange.columns if row['default_currency'] in col])
    #df_exchange['a'] = df_exchange.loc[i, 'year']
    #df_exchange['b'] = (row[[col for col in df_exchange.columns if row['default_currency'] in col]].astype("float").fillna(1))
    
    #if row['default_currency'] != [col for col in df_exchange.columns if row['default_currency'] in col]:
        #print([col for col in exchange_Rate.columns if row['default_currency'] in col])  
 '''


##################### grouped per year #########
# sum ransaction per year
grouped_year = df_water_transaction.groupby(['iati_identifier', 'title_narrative','description_narrative', 'sector_code', 'sector', 'reporting_org_narrative',
                                            'participating_org_narrative', 'year', 'default_currency']).agg({'transaction_value': ['sum']})

#  columns
grouped_year.columns = ['yearly_transaction']

# reset index to get grouped columns back
grouped_year = grouped_year.reset_index()


# making readeble the transaction value
#grouped_year['yearly_transaction'] = grouped_year.apply(lambda x: "{:,}".format(x['yearly_transaction']), axis=1)

# rename col
grouped_year.rename(columns={'yearly_transaction': 'disbursment', 'sector_code': 'sector code', 'sector': 'sector name', 
                    'reporting_org_narrative': 'publisher', 'participating_org_narrative': 'provider/buyer', 'iati_identifier': 'iati id', 'title_narrative': 'project'}, inplace=True)
# print(grouped_year['disbursment'])
grouped_last5year = grouped_year[grouped_year['year'].isin([2021, 2020, 2019, 2018, 2017]) ]

#grouped_last5year = grouped_last5year.sort_values(by=['default_currency','year'], ascending=[True, True])
#grouped_last5year.reset_index(drop=True, inplace=True)
grouped_sector_last5year = grouped_last5year.groupby(["sector code",'sector name']).agg({'disbursment': ['sum']})
grouped_sector_last5year.columns = ['sector_disbursment']
####### convert disbursment  ####
convert = pd.DataFrame()
convert['disbursment'] = (grouped_last5year['disbursment'].loc[0:6])*(grouped_rate['CHF'].loc[0])
'''
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[7:15])*(grouped_rate['CHF'].loc[1]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[15:17])*(grouped_rate['CHF'].loc[2]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[18:22])*(grouped_rate['CHF'].loc[3]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[23:32])*(grouped_rate['CHF'].loc[4]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[33:42])*(grouped_rate['DKK'].loc[5]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[43:47])*(grouped_rate['DKK'].loc[6]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[48:54])*(grouped_rate['DKK'].loc[7]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[55:59])*(grouped_rate['DKK'].loc[8]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[60:65])*(grouped_rate['DKK'].loc[9]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[66:75])*(grouped_rate['EUR'].loc[10]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[76:85])*(grouped_rate['EUR'].loc[11]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[86:98])*(grouped_rate['EUR'].loc[12]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[99:107])*(grouped_rate['EUR'].loc[13]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[108:121])*(grouped_rate['EUR'].loc[14]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[122])*(grouped_rate['GBP'].loc[15]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[123])*(grouped_rate['GBP'].loc[16]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[124:126])*(grouped_rate['GBP'].loc[17]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[127:128])*(grouped_rate['GBP'].loc[18]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[129:130])*(grouped_rate['GBP'].loc[19]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[131:140])*(grouped_rate['USD'].loc[20]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[141:152])*(grouped_rate['USD'].loc[21]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[153:169])*(grouped_rate['USD'].loc[22]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[170:183])*(grouped_rate['USD'].loc[23]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[184:197])*(grouped_rate['USD'].loc[24]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[198:199])*(grouped_rate['XDR'].loc[25]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[200:201])*(grouped_rate['XDR'].loc[26]), columns=['disbursment']))
convert = convert.append(pd.DataFrame((grouped_last5year['disbursment'].loc[202])*(grouped_rate['XDR'].loc[27]), columns=['disbursment']))
'''

##################################################################################################################


# Save data as a spreadsheet in Excel
#grouped_sector_last5year.to_csv("grouped_sector_last5year.csv")

#df_exchange.to_csv("df_exchange.csv")
#df_water.to_excel(" water sector.xlsx", sheet_name="all info", index=False)
