from utils import retrieve_data
import pandas as pd

output_file = "output.csv"
data_base = pd.read_csv(output_file)
url = "/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/abritel/annonces/Superbe Studio Calme Proche Bercy (07_05_2024 18_51_16).html"
data  = retrieve_data(url)
df = pd.DataFrame([data])
database = pd.concat([data_base, df], ignore_index=True)
database.to_csv(output_file, mode="w", header=True, index=False)