import pandas as pd
import ast

data = pd.read_csv("output.csv")
data = data.head(5)

print(data.columns)

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
def split_details(lst, keyword):
    for item in lst:
        if keyword in item:
            # Extract and return the numeric value
            return "".join(filter(str.isdigit, item))
    return None  # Return None if the keyword is not found


# Process the 'details' column
data["nb_rooms"] = data["details"].apply(
    lambda x: next((int(s.split()[0]) for s in x if "pièce" in s), None)
)
data["nb_bedrooms"] = data["details"].apply(
    lambda x: next((int(s.split()[0]) for s in x if "chambre" in s), None)
)

data["surface"] = data["details"].apply(lambda x: split_details(x, "m²"))

# data.drop(columns=["details"], inplace=True)

# # Convert extracted values to appropriate types
# data["nb_rooms"] = pd.to_numeric(data["nb_rooms"], errors="coerce")
# data["nb_bedrooms"] = pd.to_numeric(data["nb_bedrooms"], errors="coerce")
# data["surface"] = pd.to_numeric(data["surface"], errors="coerce")

# # Reordering colunms
# cols = ["title", "price"] + [
#     col for col in data.columns if col not in ["title", "price"]
# ]
# data = data[cols]

# print(data["details"])
print(data["nb_rooms"])
# print(data["nb_bedrooms"])

data.to_csv("tiny_output_processed.csv", mode="w", header=True, index=False)
