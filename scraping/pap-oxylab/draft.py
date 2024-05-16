from utils import *

scraped_data = scrape_ad("https://www.pap.fr/annonces/appartement-angers-r451801512")
scraped_data = process_outputs(scraped_data)

desc_data = process_description(scraped_data["description"])

merged_data = add_desc_content_to_df(desc_data, scraped_data)

save_to_database(merged_data)

print(merged_data.columns)
