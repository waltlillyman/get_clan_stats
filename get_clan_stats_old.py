""" 5/24/24: Get Clash Royale clan members list from Supercell API, output an Excel workbook, and post it to a Discord channel. """

import json
import pandas as pd
from dateutil import parser
from pytz import timezone
import requests
import openpyxl

def fetch_stats():
    BASE_URL = "https://api.clashroyale.com/v1"
    CLAN_TAG = "%23CY02QQ"  # St Louis United
    API_ENDPOINT = f"{BASE_URL}/clans/{CLAN_TAG}/members"

    # Bearer token which will only work from the IP address allowed for it:
    BEARER_TOKEN = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.'
                    'eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjgzOTI5NWYzLWVkYTAtNDdlYi04MW'
                    'Y3LWExOThiYjhlZDgxZSIsImlhdCI6MTcxNTY0NTYwNCwic3ViIjoiZGV2ZWxvcGVyL2ZmNjgxMzJjLTFlZmYtNzJiNC1hOWMz'
                    'LWJkODZjMDcwZDEzZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsIn'
                    'R5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5OS4yMC4xMDMuMTkyIl0sInR5cGUiOiJjbGllbnQifV19.uYUV32kywWv'
                    '5OdNmuvSxkPdn8TBSUyuMLTNwj5M3WhRXowt_GWzMEhcnh7V7KhvjVD1XQEzIKjav5GS-i5oLGA')

    # Set the headers with the bearer token
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    try:
        # Send the GET request
        response = requests.get(API_ENDPOINT, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response data
            data = response.json()
            # print(data)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise SystemExit(1) from e

    return data

def create_excel(data, filename):
    # Extract the list of items from the JSON data
    items = data['items']

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(items)

    # Convert 'lastSeen' to datetime format in Central Time Zone
    central_tz = timezone('US/Central')
    df['lastSeen'] = df['lastSeen'].apply(lambda x: parser.isoparse(x).astimezone(central_tz).strftime('%Y-%m-%d %H:%M:%S'))

    # Convert the 'Date' column to datetime
    df['lastSeen'] = pd.to_datetime(df['lastSeen'])

    # Expand the 'arena' column into separate columns
    arena_cols = pd.json_normalize(df['arena'], record_prefix='arena.')
    df = pd.concat([df, arena_cols], axis=1)
    df.drop('arena', axis=1, inplace=True)

    # Create an Excel file
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Write the DataFrame to Excel
    df.to_excel(writer, sheet_name='St Louis United Clan', index=False)

    # Get the worksheet object
    workbook = writer.book
    worksheet = writer.sheets['St Louis United Clan']

    # Define the date format as Excel-sortable:
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

    # Apply the date format to the 'lastSeen' column
    last_seen_col = df.columns.get_loc('lastSeen')
    worksheet.set_column(last_seen_col, last_seen_col, None, date_format)

    # Save the Excel file
    writer.close()

def upload_discord(workbook_name):
    # Upload the file to discord via our webhook URL:
    # For posting to co-leaders-chat channel:
    # webhook_url = "https://discord.com/api/webhooks/1240992955343306812/KpPF1S5De_CYmbBM2NbcoV5oy9HoO-Apj-CDnLbl8PSW04r0QcQhXholKf9yupJa14p7"
    # For posting to co-leaders-files channel:
    webhook_url = "https://discord.com/api/webhooks/1247722441048850444/QUKMoSEKAnfjK95YO_nAi_JJBKd2AUjSiBcxjua0WgDv1BhVVd_wxhTzEvk6jECwie7s"
    message_content = "Latest stats attached."
    payload = {
        "content": message_content
    }

    # Convert the payload to JSON string
    payload_json = json.dumps(payload)

    # Construct the files dictionary
    files = {
        "payload_json": (None, payload_json),
        "file1": open(workbook_name, "rb")
    }

    # Send the POST request
    response = requests.post(webhook_url, files=files)

    # Return the text of the response status code:
    if response.status_code == 200 or response.status_code == 204:
        return("File uploaded successfully!")
    else:
        return(f"Failed to upload file. Status code: {response.status_code}")

if __name__ == '__main__':
    workbook_name='slu_clan_members.xlsx'
    # 1. Fetch stats from Clash Royale API:
    data = fetch_stats()
    # 2. Create an Excel workbook file from the stats:
    create_excel(data, workbook_name)
    # 3. Post the Excel file to discord and print the result:
    print(upload_discord(workbook_name))

