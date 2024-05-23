import pandas as pd

# Sample DataFrame
data = pd.DataFrame(
    {
        "details": [
            ["3 pièces", "2 chambres", "50 m²"],
            ["4 pièces", "100 m²"],  # Example with missing 'chambres'
            [],  # Example with missing 'pièces'
            ["5 pièces", "3 chambres", "120 m²"],
        ]
    }
)


# Function to extract values
def extract_value(lst, keyword):
    for item in lst:
        if keyword in item:
            # Extract and return the numeric value
            return "".join(filter(str.isdigit, item))
    return None  # Return None if the keyword is not found


# Process the 'details' column
data["nb_rooms"] = data["details"].apply(lambda x: extract_value(x, "pièces"))
data["nb_bedrooms"] = data["details"].apply(lambda x: extract_value(x, "chambres"))
data["surface"] = data["details"].apply(lambda x: extract_value(x, "m²"))

# Convert extracted values to appropriate types
data["nb_rooms"] = pd.to_numeric(data["nb_rooms"], errors="coerce")
data["nb_bedrooms"] = pd.to_numeric(data["nb_bedrooms"], errors="coerce")
data["surface"] = pd.to_numeric(data["surface"], errors="coerce")

print(data)
