from pap_scraper import scrape_ad
from pap_postprocessing import process_outputs
from utils import process_description, add_desc_content_to_df, save_to_database

test_description = """
Calme et résidentiel, 1,5 km Belle-Épine, 2,5 km RER Rungis, 6 km Paris par autoroute avec bus direct Porte d'Italie à 50 m, propriétaire loue maison 118 m2 avec jardin 400 m2, comprenant :

- Rez-de-chaussée : entrée, double living, cuisine aménagée, un wc + lave-mains.

- 1er étage : palier desservant 3 chambres avec placards dont une suite parentale avec dressing, 2 salles de bains et wc.

1 garage"""

desc_data = process_description(test_description)
ad_data = scrape_ad("https://www.pap.fr/annonces/maison-rungis-ville-r437900803")
ad_data = process_outputs(ad_data)
final_data = add_desc_content_to_df(desc_data, ad_data)
for column in final_data.columns:
    print(final_data[column])

save_to_database(final_data, "pap")
