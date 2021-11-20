import pandas as pd
import os
import sys
project_path = os.environ['PROJECT_PATH']
sys.path.append(project_path + '/src')
from connection.postgress_connection import Postgress_Connection

def send_data_to_sqlite(config_data, catalog):
    """
    Função para enviar os dados preparados para base de dados, esta comentada pois não sera utilizada local
    """
    pass
    '''
    connect = Postgress_Connection(config_data['connection'])
    list_tables = config_data['tables']
    for table in list_tables:
        path_table = f"{os.environ['PROJECT_PATH']}/{catalog[table]['location']}/{table}.{catalog[table]['type']}"
        print(f"Send to database data in {path_table}")
        df = pd.read_csv(path_table)
        connect.send_dataframe(df)
    '''