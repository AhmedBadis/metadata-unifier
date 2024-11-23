import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

# Login credentials
base_url = 'https://pyrat.ukbonn.de/pyrat-test/api/v3'
payload = HTTPBasicAuth('4-e6384666747e295680e7f9d94ec53a0f55a3d569c888',
                        '20-6d803f5830ed96f3c0403b7e6b6c5f1fd4590975e2fc')

# Define the query parameters
params = {
    'k': [
        "cageid",
        "cagetype",
        "cagenumber",
        "cagelabel",
        "owner_userid",
        "owner_username",
        "owner_fullname",
        "responsible_id",
        "responsible_fullname",
        "projects",
        "rack_id",
        "room_id",
        "status",
        "num_total",
        "num_males",

        # Unused parameters
        # "category",
        # "creationdate",
        # "terminationdate",
        # "rack",
        # "area_id",
        # "area",
        # "building_id",
        # "building",
        # "num_females",
        # "comments",
        # "male_strain_id",
        # "male_strainname",
        # "female_strain_id",
        # "female_strainname",
        # "pup_strain_id",
        # "pup_strain",
        # "cage_color",
        # "cage_user_color",
    ],
    's': "cagenumber:asc",  # Example sort parameter

        # Unused sort parameters (Max 1)
        # "cagetype:asc",
        # "cagetype:desc",
        # "cagenumber:desc",
        # "cagelabel:asc",
        # "cagelabel:desc",
        # "category:asc",
        # "category:desc",
        # "creationdate:asc",
        # "creationdate:desc",
        # "owner_username:asc",
        # "owner_username:desc",
        # "owner_fullname:asc",
        # "owner_fullname:desc",
        # "projects:asc",
        # "projects:desc",
        # "responsible_fullname:asc",
        # "responsible_fullname:desc",
        # "rack:asc",
        # "rack:desc",
        # "room:asc",
        # "room:desc",
        # "area:asc",
        # "area:desc",
        # "building:asc",
        # "building:desc",
        # "male_strainname:asc",
        # "male_strainname:desc",
        # "female_strainname:asc",
        # "female_strainname:desc",
        # "pup_strain:asc",
        # "pup_strain:desc",
    'o': 0,
    'l': 100,
    'status': "open_or_empty"
}

# Start a session
session = requests.Session()

# Perform login and request data with query parameters
response = session.get(base_url + '/cages', auth=payload, params=params)

# Check for successful response
if response.status_code == 200:
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
else:
    print(f"Error: {response.status_code} - {response.text}")