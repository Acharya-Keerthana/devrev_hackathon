import os
import requests
import json
from dotenv import load_dotenv

# Load the .env file to fetch the PAT
load_dotenv()
access_token = os.getenv("PERSONAL_ACCESS_TOKEN")

# URL for API call to list work items
url = "https://api.devrev.ai/works.list"

# File path where you want to store the JSON data
file_path = "new_response_data.json"

# Get request to list work items by passing PAT as a header
try:
    response = requests.get(
        url,
        headers={
            "Authorization": access_token,
        }
    )
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

    # Parse the response JSON
    data = response.json()
    json_data = json.dumps(data, indent=2)
    print(json_data)

    # Write JSON data to file
    with open(file_path, "w") as file:
        file.write(json_data)
        print(f"Data has been successfully written to {file_path}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
