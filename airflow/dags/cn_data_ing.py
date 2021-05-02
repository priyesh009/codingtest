import pandas as pd
import os
from StringIO import StringIO
from datetime import datetime

DRI_JSON = '/home/ubuntu/airflow/cn_files/src1/'
DIR_CSV = '/home/ubuntu/airflow/cn_files/src2/'
DIR_MERGED = '~/airflow/cn_files/processed/final_{}.csv'.format(datetime.now().date())

def process_json(dir):
    "Process JSON files. Get list of files to be process from source and process them."
    df_list = []
    if os.listdir(dir):
        for file in os.listdir(dir):
            date = file.split('_')[1][:8]
            with open(dir + file,'r') as rawdata:
                jsondata= [i.strip() for i in rawdata.readlines()]

            for row in jsondata:
                #Using StringIO moulde to get rid of ValueError dur to some characters
                series = pd.read_json(StringIO(row), typ='series')
                df = pd.DataFrame(series)
                new=df.transpose()
                new['date'] = date                 #Adding Date column in DataFrame
                df_list.append(new)

        final=pd.concat(df_list) 
        final['shares'] = final['shares'].apply(lambda x: x.get('count') if type(x) != type(1.1) else 0)  # Getting Share count 
        #print(final)
        #final.to_csv('C:/Users/priye/PycharmProjects/condenast/processed/test_json.csv', index=False)
        return final
    else:
        raise FileNotFoundError


def process_csv(dir):
    "Process CSV files. Get list of files to be process from source and process them."
    df_list=[]
    if os.listdir(dir):
        for file in os.listdir(dir):
            date = file.split('_')[1][:8]
            df = pd.read_csv(dir + file)
            df['date'] = date #Adding Date column in DataFrame
            df_list.append(df)

        final=pd.concat(df_list)
        #print(final)
        #final.to_csv('C:/Users/priye/PycharmProjects/condenast/processed/test_csv.csv', index=False)
        return final
    else:
        raise FileNotFoundError


def merge_df():
    "Merge Source DataFrames and creates Final CSV file"
    df_csv = process_csv(DIR_CSV)
    df_json = process_json(DRI_JSON)
    final = pd.merge(df_csv, df_json, how='outer', on=['post_id', 'date']) # Merging CSV and JSON source files using outer join on columns post_id and date so we have all rows form both sources. 
    final = final.fillna(0) # replacing null values with 0 
    m = (final.dtypes == 'float')
    final.loc[:, m] = final.loc[:, m].astype(int) # getting rid of decimals 
    final.to_csv(DIR_MERGED, encoding='utf-8', index=False) 

