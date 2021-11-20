### Save data
1. Save data creditcard.csv in data/raw 

### Start envoriment
1. **Create conta env**

   $ conda create env   

2. **Install Libs**
    
   $ pip install -r requiremnts.txt


### How to start airflow
1. **Set AIRFLOW_HOME**

    $ export AIRFLOW_HOME= {actual-path}/config/airflow

    $ export PROJECT_PATH= {actual-path}/src


2. **Start database (Optional)**

    $ airflow initdb 


3. **Start scheduler (Optional)**

    $ airflow scheduler


4. **Start webserver**

    $ airflow webserver -p 8080


5. **Run dag**

   $  airflow backfill dataops -s 2020-06-12

### How to see mlflow server
1. **Go to mlflow path**

   $cd ./data

2. **Start ui**

   $ mlflow ui

