import pandas as pd

data = pd.read_csv(
    "/Users/mneau/Desktop/safeflat/scraping/gensdeconfiance/output.csv", nrows=5
)

# Printing the features before editing them
# print(data["subtitle"])
# print(data["author"])

# Processing subtitle
data["postcode"] = data["subtitle"].apply(lambda x: x.split(" ")[-1])
data["postcode"] = data["postcode"].apply(lambda x: x.replace("(", "").replace(")", ""))

# Processing Author
data["author"] = data["author"].apply(lambda x: "N/A" if "*" in x else x)
data["author_first_name"] = data["author"].apply(
    lambda x: x.split(" ")[0] if x != "N/A" else "N/A"
)
try:
    data["author_last_name"] = data["author"].apply(
        lambda x: x.split(" ")[1] if x != "N/A" else "N/A"
    )
except:
    data["author_last_name"] = "N/A"

data.drop(columns=["subtitle", "author"], inplace=True)

# Processing the prices
all_keys = ["Loyer", "Charges locatives", "Total par mois"]
for key in all_keys:
    data[key] = data["prices"].apply(lambda x: eval(x).get(key, "-1"))
    data[key] = data[key].apply(lambda x: x.replace("€", "").replace("\u202f", ""))
    data[key] = data[key].apply(int)

data.rename(
    columns={
        "Loyer": "loyer",
        "Charges locatives": "charges",
        "Total par mois": "total par mois",
    },
    inplace=True,
)

# Printing the features after editing them
# print(data["author_first_name"])
# print(data["author_last_name"])
# print(data["postcode"])
print(data["loyer"])
print(data["charges"])
print(data["total par mois"])
