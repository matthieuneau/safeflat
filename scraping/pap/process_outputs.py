import pandas as pd
import ast

data = pd.read_csv("output.csv")

print(data.head())

# Splitting title_and_price column
split_data = data["title_and_price"].str.rsplit("\n", expand=True)
data["title"] = split_data[0]
data["price"] = split_data[1]

data.drop(columns=["title_and_price"], inplace=True)

# Converting price to numeric
data["price"] = data["price"].apply(
    lambda x: int(x.replace("€", "").replace(".", "").strip())
)


# Splitting the details
# data["details"] = data["details"].apply(ast.literal_eval)
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

# Reordering colunms
cols = ["title", "price"] + [
    col for col in data.columns if col not in ["title", "price"]
]
data = data[cols]

print(data.head())

data.to_csv("output_processed.csv", mode="w", header=True, index=False)
