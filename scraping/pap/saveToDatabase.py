import pandas as pd
from sqlalchemy import create_engine


def save_to_database(data_collected: pd.DataFrame):
    # Convert all columns to string to avoid errors when writing to database
    data_collected = data_collected.map(str)

    db_config = {
        "host": "safeflat-scraping-data.cls8g8ie67qg.us-east-1.rds.amazonaws.com",
        "port": 3306,
        "user": "admin",
        "password": "SBerWIyVxBu229rGer6Z",
        "database": "scraping",
    }

    table_name = "pap"

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    data_collected.to_sql(name="pap", con=engine, if_exists="append", index=False)
