import instructor
from typing import Literal
from pydantic import Field
from pydantic import BaseModel
from openai import OpenAI

test_description = """En plein cœur de Charenton, proche de toutes les commodités et du bois de Vincennes.

Dans une copropriété au calme, Un très bel appartement type loft/duplex, meublé, de 59m2 au sol.

Il se compose de 3 pièces, avec au RDC un bel espace de vie, une cuisine séparée équipée, une salle d'eau avec WC.
A l'étage : deux chambres, dont une avec un filet, un coin bureau.

L'appartement dispose d'un espace extérieur."""


# Define your desired output structure
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


# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

# Extract structured data from natural language
desc_info = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=DescriptionInfo,
    messages=[{"role": "user", "content": test_description}],
)

desc_info = desc_info.model_dump()

print(desc_info)
