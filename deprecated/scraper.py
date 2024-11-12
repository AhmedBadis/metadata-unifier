import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, parse_qs

# Initialize session & perform login
session = requests.Session()
base_url = 'https://PyRAT.ukbonn.de/PyRAT-test/cgi-bin'
login_url = base_url + '/login.py'
payload = {'username': 'some_username', 'password': 'some_password'}
response = session.post(login_url, data=payload)

# Check if login was successful
if response.ok:
    # Extract session ID from the URL if present
    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)
    session_id = query_params.get('sessionid')

    # URL of the page with the table
    data_url = base_url + '/mainpage.py?sessionid={session_id[0]}'

    # Fetch the page content using the authenticated session
    response = session.get(data_url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table
    table = soup.find('table', class_='standard-table zebra-style')
    if table:
        # Extract rows
        rows = table.find_all('tr')

        # Prepare a list to hold the table data
        table_data = []

        # Loop through rows and extract cell data
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            table_data.append(cols)

        # Write the data to a JSON file
        with open('table_data.json', 'w', encoding='utf-8') as file:
            json.dump(table_data, file, ensure_ascii=False, indent=4)

        print('Table data has been written to table_data.json')
    else:
        print('No table found on the page.')
else:
    print("Login failed. Check your credentials and URL.")