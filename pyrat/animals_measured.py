from common_request import perform_request
from animals import params

perform_request('/animals', params, measured=True)