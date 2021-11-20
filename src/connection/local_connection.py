import pandas as pd
import os

class Local_Connection:
    def __init__(self, connect_data, catalog_data):
        self.catalog_data = catalog_data
        self.connect_data = connect_data

    def send_dataframe(self, df):
        df.to_sql(df, con=self.engine, if_exists='replace')

    def read_df(self, table_name):
        location = self.catalog_data[table_name]['location']
        table_type = self.catalog_data[table_name]['type']
        table_path = f"{os.environ['PROJECT_PATH']}/{location}/{table_name}.{table_type}"
        df = pd.read_csv(table_path)
        return df

    def save_df(self, df, table_name):
        location = self.catalog_data[table_name]['location']
        table_type = self.catalog_data[table_name]['type']
        table_path = f"{os.environ['PROJECT_PATH']}/{location}/{table_name}.{table_type}"
        if table_type == 'csv':
            df.to_csv(table_path)
        else:
            print("Invalid format")