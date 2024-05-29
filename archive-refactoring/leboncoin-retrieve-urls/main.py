from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    num_pages = 3
    for i in range(1, num_pages):
        urls = retrieve_urls(
            f"https://www.leboncoin.fr/recherche?category=10&locations=Strasbourg_67000__48.58504_7.73642_5000_1000&real_estate_type=1,2&owner_type=private&page={i}"
        )
        print(urls)
        for url in urls:
            try:
                scraped_data = scrape_ad(url)
                print('Scraped ad:', scraped_data)

                desc_data = process_description(scraped_data["description"])

                merged_data = add_desc_content_to_df(desc_data, scraped_data)

                data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output_processed.csv')

                df_concatene = pd.concat([merged_data, data_bdd], ignore_index=True)
                df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output_processed.csv')

                #save_to_database(merged_data)
            except Exception as e:
                print(f"An error occrued while processing the ad: {url}", "\n", e)

    return {"statusCode": 200, "body": json.dumps("Lambda executed successfully!")}


if __name__ == "__main__":
    handler(None, None)
    