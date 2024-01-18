import requests


def download_html(url, file_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(response.text)
            print(f"HTML content of {url} has been saved to {file_name}")

    except requests.RequestException as e:
        print(f"Error during requests to {url}: {str(e)}")


# Example usage
url = "https://www.leboncoin.fr/offre/locations/2480020014"  # Replace with your target URL
file_name = "webpage.html"  # Replace with your desired file name
download_html(url, file_name)
