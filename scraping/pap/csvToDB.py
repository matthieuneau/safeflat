import pandas as pd
from sqlalchemy import create_engine

db_config = {
    "host": "safeflat-scraping-data.cls8g8ie67qg.us-east-1.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": "SBerWIyVxBu229rGer6Z",
    "database": "scraping",
}

csv_file_path = "scraping/pap/output.csv"

table_name = "pap"

# Creating a connection string for SQLAlchemy
connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

engine = create_engine(connection_string)

df = pd.read_csv(csv_file_path)

# Might need to set chunksize if error because writing too many rows at once
# Might need to specify schema if table columns and .csv columns don't match
df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
