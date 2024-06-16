import requests
from openai import OpenAI
import instructor
import os
import pandas as pd
import dotenv
from sqlalchemy import create_engine
from pydantic import BaseModel, Field
from typing import Literal


dotenv.load_dotenv()


def fetch_html_with_oxylab(page_url: str) -> str:
    proxies = {
        "http": f"http://{os.getenv('OXYLAB_USERNAME')}:{os.getenv('OXYLAB_PASSWORD')}@unblock.oxylabs.io:60000",
        "https": f"http://{os.getenv('OXYLAB_USERNAME')}:{os.getenv('OXYLAB_PASSWORD')}@unblock.oxylabs.io:60000",
    }

    response = requests.request(
        "GET",
        page_url,
        verify=False,  # Ignore the certificate
        proxies=proxies,
    )

    return response.text


def add_desc_content_to_df(
    processed_desc: pd.DataFrame, processed_ad: pd.DataFrame
) -> pd.DataFrame:
    """Merges all the information from the processed description and the processed ad with one simple rule:
    Consider that the data from the ad is more reliable than the data from the description. So if there is
    a conflict between the two, keep the data from the ad.

    Args:
        processed_desc (pd.DataFrame): processed description data
        processed_ad (pd.DataFrame): processed ad data

    Returns:
        pd.DataFrame: merged data
    """
    for col in processed_desc.columns:
        if col not in processed_ad.columns:
            processed_ad[col] = processed_desc[col]

    return processed_ad


### TO BE EDITED ###
def save_to_database(data_collected: pd.DataFrame, website: str):
    # Convert all columns to string to avoid errors when writing to database
    data_collected = data_collected.map(str)

    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": 3306,
        "user": "admin",
        "password": os.getenv("DB_PASSWORD"),
        "database": "scraping",
    }

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    data_collected.to_sql(name=website, con=engine, if_exists="append", index=False)


class DescriptionInfo(BaseModel):
    surface: float = Field(
        ..., title="Surface", description="The surface area in square meters"
    )
    nb_rooms: int = Field(
        ..., title="Number of Rooms", description="The number of rooms"
    )
    piscine: Literal["yes", "no"] = Field(
        ...,
        title="Swimming Pool",
        description="Indicates the presence of a swimming pool. Returns 'yes' if present, 'no' otherwise",
    )
    type_de_bien: Literal["apartment", "house"] = Field(
        ...,
        title="Property Type",
        description="The type of property. It can only be an apartment or a house",
    )
    nb_bedrooms: int = Field(
        ..., title="Number of Bedrooms", description="The number of bedrooms"
    )
    parking: Literal["yes", "no"] = Field(
        ...,
        title="Parking",
        description="Indicates the presence of a private parking space. Returns 'yes' if present, 'no' otherwise",
    )
    quartier: str = Field(
        ...,
        title="Neighborhood",
        description="The name of the neighborhood where the property is located",
    )
    meuble: Literal["yes", "no"] = Field(
        ...,
        title="Furnished",
        description="Indicates if the property is furnished. Returns 'yes' if furnished, 'no' otherwise",
    )
    nombre_d_etages: int = Field(
        ...,
        title="Number of Floors",
        description="The number of floors in the property",
    )
    numero_d_etage: int = Field(
        ...,
        title="Floor Number",
        description="The floor number where the property is located if it's an apartment",
    )
    ascenseur: Literal["yes", "no"] = Field(
        ...,
        title="Elevator",
        description="Indicates the presence of an elevator if the property is an apartment in a building. Returns 'yes' if there is an elevator, 'no' otherwise",
    )
    cave: Literal["yes", "no"] = Field(
        ...,
        title="Cellar",
        description="Indicates the presence of a cellar. Returns 'yes' if there is a cellar, 'no' otherwise",
    )
    terrasse: Literal["yes", "no"] = Field(
        ...,
        title="Terrace",
        description="Indicates the presence of a terrace. Returns 'yes' if there is a terrace, 'no' otherwise",
    )


def process_description(description: str) -> pd.DataFrame:

    client = instructor.from_openai(OpenAI())

    # Extract structured data from natural language
    desc_info = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=DescriptionInfo,
        messages=[{"role": "user", "content": description}],
    )

    desc_info_dict = desc_info.model_dump()
    desc_info_df = pd.DataFrame(desc_info_dict, index=[0])

    return desc_info_df
