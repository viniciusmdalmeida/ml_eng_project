#Importando bibliotecas nescessárias 
import pandas as pd 
from datetime import datetime
import os

#Importanto bibliotecas internas

import sys
project_path = os.environ['PROJECT_PATH']
sys.path.append(project_path + '/src')
from connection.local_connection import Local_Connection

def split_data(config_data, catalog_data):
    connection = Local_Connection(config_data, catalog_data)
    master_table = connection.read_df('creditcard')

    #pegando amostra dos dados
    percent_sample = config_data['split_data']['percent_sample']
    ponto_corte = int(len(master_table)*percent_sample)
    master_part = master_table[:ponto_corte]
  
    #Separando treino e teste
    percent_train = config_data['split_data']['percent_train']
    ponto_corte = int(len(master_table)*percent_train)
    train_index = master_table[:ponto_corte].index
    test_index = master_table[ponto_corte:].index

    return {'train_index':train_index,'test_index':test_index}
