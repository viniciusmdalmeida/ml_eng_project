#Importando bibliotecas nescessárias 
import pandas as pd 
import yaml
import psycopg2
from sqlalchemy import create_engine
import sys
from sklearn.preprocessing import StandardScaler

import os
project_path = os.environ['PROJECT_PATH']
sys.path.append(project_path + '/src')
from connection.local_connection import Local_Connection

def prep_data(config_data, catalog_data):
    connection = Local_Connection(config_data, catalog_data)
    raw_table = connection.read_df('creditcard')

    # remove columns
    raw_table = raw_table.drop('Time',axis=1)

    # normalized Amount column
    raw_table['Amount'] = StandardScaler().fit_transform(raw_table['Amount'].values.reshape(-1, 1))

    # balance data
    class_zero_data = raw_table[raw_table['Class'] == 0]
    class_one_data = raw_table[raw_table['Class'] == 1]
    class_zero_data = class_zero_data.sample(len(class_one_data))
    balance_data = pd.concat([class_one_data, class_zero_data]).sample(frac=1)

    # Reingestão
    connection.save_df(balance_data,'creditcard_silver')

