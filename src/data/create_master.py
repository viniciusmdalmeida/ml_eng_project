import pandas as pd
import yaml
import psycopg2
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler

import sys
import os
project_path = os.environ['PROJECT_PATH']
sys.path.append(project_path + '/src')
from connection.local_connection import Local_Connection

def create_master(config_data, catalog_data):
    list_df_name = config_data['list_dataframes']

    # create connection
    connection = Local_Connection(config_data, catalog_data)

    #concat list df
    list_df = []
    for table_name in list_df_name:
        df = connection.read_df(table_name)
        list_df.append(df)

    master_table = pd.concat(list_df,axis=1)

    #save df
    connection.save_df(master_table, 'master_table')
