#Importando bibliotecas nescessárias 
import pandas as pd 
from datetime import datetime

#Biliotecas internas
import os
os.chdir(os.path.dirname(__file__))
import sys
src_path = '../../src'
sys.path.append(src_path)
from modeling.models import *
from modeling.test import *
from modeling.save import *
from utils.dag_utils import *
from connection.local_connection import Local_Connection

def run_model(config_model, catalog_data, model_name, config_data, train_index, teste_index):
    #get data
    connection = Local_Connection(config_data, catalog_data)
    master_table = connection.read_df('creditcard')

    #slip data
    X = master_table.drop(config_data['split_data']['y'],axis=1)
    y = master_table[config_data['split_data']['y']] 
    #Modeling
    #buscado a classe com eval e iniciando os parametros
    print(f"Treinando modelo {model_name}")
    model_dict = config_model['models'][model_name]
    model_class = eval(model_dict['class'])
    paramns = model_dict['params']
    model = model_class(**paramns)
    #Tests 
    print(f"Testando o modelo {model_name}")
    test_func = eval(config_model['test']['func'])
    result = test_func(model,X,y,config_model['test'])
    print(f"{model_name} Teste_finalizado!")
    #Save files
    save_dict = config_model['save']
    if type(save_dict['save_func']) == str:
        save_dict['save_func'] = [save_dict['save_func']]
    for func_name in save_dict['save_func']:
        save_func = eval(func_name)
        save_func(model,result,config_model,model_name) 
