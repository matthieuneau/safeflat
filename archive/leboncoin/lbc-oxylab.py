import requests
from bs4 import BeautifulSoup

# Define proxy dict. Don't forget to put your real user and pass here as well.

username = "matycake"
password = "Safeflat123__"

proxies = {
    "http": f"http://{username}:{password}@unblock.oxylabs.io:60000",
    "https": f"http://{username}:{password}@unblock.oxylabs.io:60000",
}

response = requests.request(
    "GET",
    "https://www.leboncoin.fr/offre/locations/2498244792",
    verify=False,  # Ignore the certificate
    proxies=proxies,
)

html_doc = response.text

soup = BeautifulSoup(html_doc, "html.parser")

title = soup.select_one("#grid > article > div:nth-child(2) > div > h1")

print("title", title.get_text())

specs = soup.select_one(
    "#grid > article > div:nth-child(2) > div > div.flex.flex-wrap > p"
)
print("specs", specs.get_text())

price = soup.select_one(
    "#grid > article > div:nth-child(2) > div > div.flex.flex-wrap > div.mr-md.flex.flex-wrap.items-center.justify-between > div > p"
)
print("price", price.get_text())

description = soup.select_one(
    "#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-1 > div > p"
)
print("description", description.get_text())

author = soup.find(class_="break-words font-bold text-body-1")  # needs minor fixes
print("author", author.get_text())

element_titles = []  # doesn't capture all elements because of "see more button"
parent_divs = soup.select(
    "#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\\/dim-4.lg\\:mx-md.row-start-4"
)
for parent_div in parent_divs:
    child_divs = parent_div.select("div > div > div > div > p")
    element_titles.extend([div.text for div in child_divs])

# print(
#     soup.select_one(
#         "#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > div > div:nth-child(20) > div > div > span"
#     )
# )

element_values = []
for i in range(14):
    # print(i)
    elem = soup.select_one(
        f"#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > div > div:nth-child({i}) > div > div > span"
    )
    print(elem)
    if elem is None:
        continue
    else:
        element_values.append(elem.get_text())

print(
    soup.select_one(
        f"#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > div > div:nth-child(7) > div > div > span"
    )
)
print("elements_values", element_values)
print("elements_titles", element_titles)

# Save returned HTML to result.html file
with open("/Users/mneau/Desktop/safeflat/oxylab/result.html", "w") as f:
    f.write(response.text)
