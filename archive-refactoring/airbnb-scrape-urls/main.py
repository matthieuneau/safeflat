from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    html_page = fetch_html_with_oxylab('https://www.airbnb.fr/s/Strasbourg--France/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=Strasbourg%2C%20France&date_picker_type=calendar&checkin=2024-06-08&checkout=2024-06-09&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=1&zoom_level=15&room_types%5B%5D=Entire%20home%2Fapt&adults=3&place_id=ChIJwbIYXknIlkcRHyTnGDFIGpc&search_mode=regular_search&flexible_date_search_filter_type=6')
    with open("/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/abritel-scrape-urls/annonces/listing_annonces.html", "w", encoding="utf-8") as file:
        file.write(html_page)

    # num_pages = 2
    # for i in range(1, num_pages):
    #     urls = retrieve_urls(
    #         f"https://www.airbnb.fr/s/Strasbourg--France/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=Strasbourg%2C%20France&date_picker_type=calendar&checkin=2024-06-08&checkout=2024-06-09&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=1&zoom_level=15&room_types%5B%5D=Entire%20home%2Fapt&adults=3&place_id=ChIJwbIYXknIlkcRHyTnGDFIGpc&search_mode=regular_search&flexible_date_search_filter_type=6"
    #     )
    #     print(urls)
        # for url in urls:
        #     try:
        #         scraped_data = scrape_ad(url)
        #         print('Scraped ad:', scraped_data)

        #         desc_data = process_description(scraped_data["description"])

        #         merged_data = add_desc_content_to_df(desc_data, scraped_data)
        #         merged_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/airbnb-scrape-urls/outputs_csv/output_processed.csv')

        #         #data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output_processed.csv')

        #         #df_concatene = pd.concat([merged_data, data_bdd], ignore_index=True)
        #         #df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output_processed.csv')

        #         #save_to_database(merged_data)
        #     except Exception as e:
        #         print(f"An error occrued while processing the ad: {url}", "\n", e)

    return {"statusCode": 200, "body": json.dumps("Lambda executed successfully!")}


if __name__ == "__main__":
    handler(None, None)