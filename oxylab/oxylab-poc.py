import requests

# Define proxy dict. Don't forget to put your real user and pass here as well.

username = "matycake"
password = "Safeflat123__"

proxies = {
    "http": f"http://{username}:{password}@unblock.oxylabs.io:60000",
    "https": f"http://{username}:{password}@unblock.oxylabs.io:60000",
}

response = requests.request(
    "GET",
    "https://www.leboncoin.fr/offre/locations/2574311160",
    verify=False,  # Ignore the certificate
    proxies=proxies,
)

# Print result page to stdout
# print(response.text)
# print(type(response))

# Save returned HTML to result.html file
with open("/Users/mneau/Desktop/safeflat/oxylab/result.html", "w") as f:
    f.write(response.text)
