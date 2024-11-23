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

html_output = response.text

pprint(html_output)