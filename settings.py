 settings.py 

import os

# For fetch_stats():
BASE_URL = https://api.clashroyale.com/v1
CLAN_TAG = os.getenv('CLAN_TAG')
API_ENDPOINT = f{BASE_URL}/clans/{CLAN_TAG}/members

# Bearer token which will only work from the IP address allowed for it:
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# For create_excel():
MY_TIMEZONE = 'US/Central'
WORKBOOK_NAME = os.getenv('WORKBOOK_NAME')
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME')

# For upload_discord():
MESSAGE_CONTENT = 'Latest stats attached.'
# For posting to co-leaders-files channel:
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
