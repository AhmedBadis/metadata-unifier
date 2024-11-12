import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

# Login credentials
base_url = 'https://pyrat.ukbonn.de/pyrat-test/api/v3'
payload = HTTPBasicAuth('4-e6384666747e295680e7f9d94ec53a0f55a3d569c888',
                        '20-6d803f5830ed96f3c0403b7e6b6c5f1fd4590975e2fc')

# Start a session
session = requests.Session()

# Perform login
response = session.get(base_url + '/docs', auth=payload)

json_output = response.text

# Get the desired filename from console input
filename = input("Enter the name for the output file (without extension): ")

# Create the full path for the JSON file
json_output_path = f"Exports/{filename}.json"

# Save JSON to a file
with open(json_output_path, "w") as json_file:
    json_file.write(json_output)

# Print or save the JSON output
print(f"JSON output saved to {json_output_path}")

pprint(json_output)