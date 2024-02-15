#!/usr/bin/env python
import os
import argparse 
import pandas as pd
import fastparquet
from pyarrow import parquet
from time import time
from sqlalchemy import create_engine

pd.__version__

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.database_name
    table_name = params.table_name
    url = params.url

    # Download the parquet
    parquet_name = "output.parquet"
    os.system(f"wget {url} -O {parquet_name}")

    # Create DB Engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    
    # Read parquet file
    pq_file = parquet.ParquetFile(parquet_name)

    # Iterate through file
    batches = pq_file.iter_batches()
    df = next(batches).to_pandas()
    pd.to_datetime(df.tpep_pickup_datetime)
    pd.to_datetime(df.tpep_dropoff_datetime)

    print(df.head(10))

    # Create table
    df.to_sql(name=table_name, con=engine, if_exists="replace")

    while True:
        start_time = time()
        
        try:
            df = next(batches).to_pandas()
        except Exception:
            break
            
        pd.to_datetime(df.tpep_pickup_datetime)
        pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists="append")

        end_time = time()
        print("Inserting chunk.. took % .3f seconds " % (end_time - start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest Parquet data to postgres")

    # user, password, host, port, database name, table name, url of csv
    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="enter host name")
    parser.add_argument("--port", help="enter port name")
    parser.add_argument("--database_name", help="enter database name")
    parser.add_argument("--table_name", help="enter name of table")
    parser.add_argument("--url", help="enter url of csv")

    args = parser.parse_args()

    main(args)
