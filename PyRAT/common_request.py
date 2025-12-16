import os
import requests
import psutil
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from pprint import pprint

# Load environment variables once
load_dotenv()

BASE_URL = os.getenv('PYRAT_BASE_URL')
AUTH = HTTPBasicAuth(
    os.getenv('PYRAT_AUTH_USERNAME'),
    os.getenv('PYRAT_AUTH_PASSWORD')
)

def perform_request(endpoint: str, params: dict = None, measured: bool = False):
    """
    Generic request handler for Pyrat API endpoints.
    If measured=True, also prints memory usage and response time.
    """
    session = requests.Session()

    # Measurement before request
    if measured:
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / (1024 ** 2)  # MB

    response = session.get(BASE_URL + endpoint, auth=AUTH, params=params)

    # Measurement after request
    if measured:
        memory_after = process.memory_info().rss / (1024 ** 2)  # MB
        response_time = response.elapsed.total_seconds()

        print(f"Memory Usage Before: {memory_before:.2f} MB")
        print(f"Memory Usage After: {memory_after:.2f} MB")
        print(f"Memory Difference: {memory_after - memory_before:.2f} MB")
        print(f"Response Time: {response_time:.2f} seconds")

    if response.status_code == 200:
        json_output = response.text
        filename = input("Enter the name for the output file (without extension): ")
        json_output_path = f"exports/{filename}.json"

        with open(json_output_path, "w") as json_file:
            json_file.write(json_output)

        print(f"JSON output saved to {json_output_path}")
        pprint(json_output)
    else:
        print(f"Error: {response.status_code} - {response.text}")