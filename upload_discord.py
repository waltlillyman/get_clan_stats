import settings as s
import json
import requests

def upload_discord():
    # Upload the file to discord via our webhook URL:

    payload = {
        "content": s.MESSAGE_CONTENT
    }

    # Convert the payload to JSON string
    payload_json = json.dumps(payload)

    # Construct the files dictionary
    files = {
        "payload_json": (None, payload_json),
        "file1": open(s.WORKBOOK_NAME, "rb")
    }

    # Send the POST request
    response = requests.post(s.WEBHOOK_URL, files=files)

    # Check the response status code
    if response.status_code == 200 or response.status_code == 204:
        return 'Message sent successfully!'
    else:
        return f'Failed to send message. Status code: {response.status_code}'
