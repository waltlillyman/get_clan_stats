import settings as s
import requests

def fetch_stats():
    # Set the headers with the bearer token
    headers = {
        "Authorization": f"Bearer {s.BEARER_TOKEN}"
    }

    try:
        # Send the GET request
        response = requests.get(s.API_ENDPOINT, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response data
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return false

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise SystemExit(1) from e

