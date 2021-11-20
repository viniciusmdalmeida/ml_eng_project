#Importando bibliotecas nescessárias 
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def read_master(config_data):
    #Conectando com os dados
    connect_data = config_data['connection']
    textEngine = f"{connect_data['driver']}://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}"
    #Lendo dados em pandas
    master_table = pd.read_sql_table('master_table',textEngine)
    return master_table