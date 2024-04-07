import pandas as pd

data = pd.read_csv("/Users/mneau/Desktop/safeflat/scraping/pap/output.csv")

print(data["location"])
