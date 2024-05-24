import pandas as pd
from sqlalchemy import create_engine


def read_from_database(query: str) -> pd.DataFrame:
    db_config = {
        "host": "safeflat-scraping-data.cls8g8ie67qg.us-east-1.rds.amazonaws.com",
        "port": 3306,
        "user": "admin",
        "password": "SBerWIyVxBu229rGer6Z",
        "database": "scraping",
    }

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    df = pd.read_sql_query(query, con=engine)

    return df
