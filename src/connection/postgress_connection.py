from sqlalchemy import create_engine

class Postgress_Connection:
    def __init__(self, connect_data, catalog_data):
        self.catalog_data = catalog_data
        self.connect_data = connect_data
        self.create_engine()

    def create_engine(self):
        # get config data
        drive = self.connect_data['driver']
        user = self.connect_data['user']
        passw = self.connect_data['password']
        host = self.connect_data['host']
        port = self.connect_data['port']
        database = self.connect_data['database']

        # send df to database sqlite
        textEngine = f"{drive}://{user}:{passw}@{host}:{port}/{database}"
        self.engine = create_engine(textEngine, echo=False)

    def send_dataframe(self, df):
        df.to_sql(df, con=self.engine, if_exists='replace')

    def read_df(self, table_name):
        pass