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
        "animalid",  # Example return parameter
        "eartag_or_id",
        "state",
        "origin_name",
        "sex",
        "species_name",
        "sacrifice_reason_name",
        "sacrifice_comment",
        "datesacrificed",
        "cagenumber",
        "room_name",
        "building_name",
        "age_days",
        "dateborn",
        "comments",
        "strain_id",
        "strain_name",

        # Unused parameters
        # "pupid",
        # "prefix",
        # "labid",
        # "cohort_id",
        # "rfid",
        # "species_weight_unit",
        # "sacrifice_actor_username",
        # "sacrifice_actor_fullname",
        # "cagetype",
        # "cagelabel",
        # "cage_owner_username",
        # "cage_owner_fullname",
        # "rack_description",
        # "area_name",
        # "responsible_id",
        # "responsible_fullname",
        # "owner_userid",
        # "owner_username",
        # "owner_fullname",
        # "age_weeks",
        # "date_last_comment",
        # "generation",
        # "gen_bg_id",
        # "gen_bg",
        # "strain_name_id",
        # "strain_name_with_id",
        # "mutations",
        # "genetically_modified",
        # "parents",
        # "licence_title",
        # "licence_id",
        # "licence_number",
        # "classification_id",
        # "classification",
        # "pregnant_days",
        # "plug_date",
        # "wean_date",
        # "projects",
        # "requests",
        # "weight",
        # "animal_color",
        # "animal_user_color",
        # "import_order_request_id",
    ],
    's': "species_name:asc",  # Example sort parameter

        # Unused sort parameters (Max 1)
        # "eartag_or_id:asc",
        # "eartag_or_id:desc",
        # "prefix:asc",
        # "prefix:desc",
        # "labid:asc",
        # "labid:desc",
        # "cohort_id:asc",
        # "cohort_id:desc",
        # "origin_name:asc",
        # "origin_name:desc",
        # "sex:asc",
        # "sex:desc",
        # "species_name:asc",
        # "species_name:desc",
        # "datesacrificed:asc",
        # "datesacrificed:desc",
        # "cagenumber:asc",
        # "cagenumber:desc",
        # "cagelabel:asc",
        # "cagelabel:desc",
        # "cage_owner_username:asc",
        # "cage_owner_username:desc",
        # "cage_owner_fullname:asc",
        # "cage_owner_fullname:desc",
        # "rack_description:asc",
        # "rack_description:desc",
        # "room_name:asc",
        # "room_name:desc",
        # "area_name:asc",
        # "area_name:desc",
        # "building_name:asc",
        # "building_name:desc",
        # "responsible_fullname:asc",
        # "responsible_fullname:desc",
        # "owner_username:asc",
        # "owner_username:desc",
        # "owner_fullname:asc",
        # "owner_fullname:desc",
        # "age_days:asc",
        # "age_days:desc",
        # "age_weeks:asc",
        # "age_weeks:desc",
        # "dateborn:asc",
        # "dateborn:desc",
        # "date_last_comment:asc",
        # "date_last_comment:desc",
        # "strain_name:asc",
        # "strain_name:desc",
        # "strain_name_id:asc",
        # "strain_name_id:desc",
        # "strain_name_with_id:asc",
        # "strain_name_with_id:desc",
        # "licence_title:asc",
        # "licence_title:desc",
        # "licence_id:asc",
        # "licence_id:desc",
        # "licence_number:asc",
        # "licence_number:desc",
        # "classification_id:asc",
        # "classification_id:desc",
        # "classification:asc",
        # "classification:desc",
        # "pregnant_days:asc",
        # "pregnant_days:desc",
        # "plug_date:asc",
        # "plug_date:desc",
        # "wean_date:asc",
        # "wean_date:desc",
        # "projects:asc",
        # "projects:desc",
        # "weight:asc",
        # "weight:desc",
        # "import_order_request_id:asc",
        # "import_order_request_id:desc",
    'o': 0,  # Number of items to skip from the beginning
    'l': 100,  # Maximum amount of returned items
    'status': "active"  # Animal status
}

# Start a session
session = requests.Session()

# Perform login and request data with query parameters
response = session.get(base_url + '/animals', auth=payload, params=params)

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



import psutil
import os

# Measure memory usage before and after the API call
process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 ** 2)  # in MB

# Perform the API request
response = session.get(base_url + '/animals', auth=payload, params=params)

memory_after = process.memory_info().rss / (1024 ** 2)  # in MB

print(f"Memory Usage Before: {memory_before} MB")
print(f"Memory Usage After: {memory_after} MB")
print(f"Memory Difference: {memory_after - memory_before} MB")
response_time = response.elapsed.total_seconds()
print(f"Response Time: {response_time} seconds")