from common_request import perform_request

# Define the query parameters
params = {
    'k': ["id", "name", "status"],
    's': "name:asc",

        # Unused sort parameters (Max 1)
        # "cagetype:asc",
        #"id:asc",
        #"id:desc",
        #"name:desc",
    'o': 0,
    'l': 100,
    'status': "active"
}

perform_request('/species', params)