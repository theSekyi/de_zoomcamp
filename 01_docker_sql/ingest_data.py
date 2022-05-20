#!/usr/bin/env python
# coding: utf-8


import csv
import pandas as pd
from sqlalchemy import create_engine
import argparse
import urllib.request

def download_csv(url,csv_name):
    urllib.request.urlretrieve(url, csv_name)


def add_data_to_db_in_chunks(df_iter,table_name,engine):
    count = 0
    while True:
        df = next(df_iter)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        print(f"inserted chunck {count}")
        count += 1

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "output.csv"

    # download csv
    download_csv(url,csv_name)
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    df = pd.read_csv(csv_name,nrows=100)
    cols = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
    df[cols] = df[cols].apply(pd.to_datetime, errors='coerce')
    df_iter = pd.read_csv(csv_name, parse_dates=cols, iterator=True, chunksize=100000)
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    add_data_to_db_in_chunks(df_iter,table_name,engine)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table where the results are written to')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()
    
    main(args)






