import re
import requests
from common_request import BASE_URL, AUTH

# First request to /docs to extract the URL
session = requests.Session()
response = session.get(BASE_URL + '/docs', auth=AUTH)
html_output = response.text

# Regex to extract the URL
url_pattern = r"url:\s*'([^']+)'"
match = re.search(url_pattern, html_output)

if match:
    extracted_url = match.group(1)
    print(f"Extracted URL: {extracted_url}")

    # Perform second request to extracted URL
    response = session.get(extracted_url, auth=AUTH)
    if response.status_code == 200:
        json_output = response.text
        filename = input("Enter the name for the output file (without extension): ")
        json_output_path = f"exports/{filename}.json"

        with open(json_output_path, "w") as json_file:
            json_file.write(json_output)

        print(f"JSON output saved to {json_output_path}")
        from pprint import pprint
        pprint(json_output)
    else:
        print(f"Error: {response.status_code} - {response.text}")
else:
    print("URL not found.")