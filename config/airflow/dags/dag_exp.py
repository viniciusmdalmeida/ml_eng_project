import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
import yaml
import os

import sys
project_path = os.environ['PROJECT_PATH']
sys.path.append(project_path + '/src')

from utils.dag_utils import *
from modeling.save import *
from modeling.run import *
from data.prep_data import *
from data.split_data import *
from data.create_master import *
from tests.unit_test import *
from data.ingestion import send_data_to_sqlite

args = {
    'owner': 'serasa',
    'start_date': days_ago(2),
    'email': ['example@serasa.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

###############################
# Read config File
###############################
#Paths
src_path = f"{project_path}/src"
conf_path = f"{project_path}/config"
conf_model_path = f'{conf_path}/model_config.yaml'
conf_data_path = f'{conf_path}/data_config.yaml'
conf_test_path = f'{conf_path}/unit_test_config.yaml'
catalog_path = f'{conf_path}/catalog.yaml'

#Lendo arquivos de configuração
config_model_file = open(conf_model_path)
config_model = yaml.load(config_model_file, Loader=yaml.FullLoader)
config_model_file.close()

config_data_file = open(conf_data_path)
config_data = yaml.load(config_data_file, Loader=yaml.FullLoader)
config_data_file.close()

catalog_file = open(catalog_path)
catalog_data = yaml.load(catalog_file, Loader=yaml.FullLoader)
catalog_file.close()

config_test_file = open(conf_test_path)
config_test = yaml.load(config_test_file, Loader=yaml.FullLoader)
config_test_file.close()

##############################
#   Create Dag
##############################
dag = DAG(
    dag_id='dag_exp',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=60)
)

##############################
#    Tasks Functions
##############################
def ingestion_data(**kwargs):
  config_data = kwargs['config_data']
  catalog_data = kwargs['catalog_data']
  send_data_to_sqlite(config_data, catalog_data)

def prep_data_func(**kwargs):
  print("------- Start Prep Data --------")
  config_data = kwargs['config_data']
  catalog_data = kwargs['catalog_data']
  if config_data['prep_data']['func'] is not None:
    func = eval(config_data['prep_data']['func'])
    func(config_data, catalog_data)


def create_master_func(**kwargs):
  config_data = kwargs['config_data']
  catalog_data = kwargs['catalog_data']
  if config_data['master_table_func'] is not None:
    func = eval(config_data['prep_data']['func'])
    func(config_data,catalog_data)


def unit_test_func(**kwargs):
  config_data = kwargs['config_data']
  config_test = kwargs['config_test']
  unit_test(config_data,config_test) 


def split_func(**kwargs):
  config_data = kwargs['config_data']
  catalog_data = kwargs['catalog_data']
  func = eval(config_data['split_data']['func'])
  return func(config_data, catalog_data)


def model_test_func(**kwargs):
  ti = kwargs['ti']
  split_index = ti.xcom_pull(task_ids='split_data')
  print("Model",split_index['train_index'])
  run_model(kwargs['config_model'],kwargs['catalog_data'], kwargs['model_name'],
            kwargs['config_data'],split_index['train_index'],split_index['test_index'])
  #return func(config['prep_data'],train_index,test_index)


def compare_func(**kwargs):
  return 'test'

##############################
#   Create Tasks
##############################
task_ingestion = PythonOperator(
    task_id='ingestion_data',
    python_callable=ingestion_data,
    provide_context=True,
    op_kwargs={'config_data':config_data,
               'catalog_data':catalog_data},
    dag=dag)

task_prep_data = PythonOperator(
    task_id='prep_data',
    python_callable=prep_data_func,
    provide_context=True,
    op_kwargs={'config_data':config_data,
               'catalog_data':catalog_data},
    dag=dag)

task_master_table = PythonOperator(
    task_id='create_master_table',
    python_callable=create_master_func,
    provide_context=True,
    op_kwargs={'config_data':config_data,
               'catalog_data':catalog_data},
    dag=dag)

task_unit_test = PythonOperator(
    task_id='unit_test',
    python_callable=unit_test_func,
    provide_context=True,
    op_kwargs={'config_data':config_data,'config_test':config_test},
    dag=dag)

task_split_data = PythonOperator(
    task_id='split_data',
    python_callable=split_func,
    provide_context=True,
    op_kwargs={'config_data':config_data,
               'catalog_data':catalog_data},
    dag=dag)

def create_task_model_test(name,config):
  task_model_test = PythonOperator(
    task_id='test_'+str(name),
    python_callable=model_test_func,
    provide_context=True,
    op_kwargs={'config_model':config_model,'catalog_data':catalog_data,
               'model_name':name,'config_data':config_data},
    dag=dag)
  return task_model_test

task_save = PythonOperator(
    task_id='compare',
    python_callable=compare_func,
    provide_context=True,
    dag=dag)

###############################
# Make WorkFlow
###############################
list_models_tasks = []
for model_name in config_model['models']:
  task_test = create_task_model_test(model_name,config_model['models'][model_name])
  list_models_tasks.append(task_test)

task_prep_data >> task_unit_test >> task_master_table >>task_split_data >> list_models_tasks >> task_save



