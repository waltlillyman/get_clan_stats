import settings as s
import pandas as pd
from dateutil import parser
from pytz import timezone

def create_excel(data):
    # Extract the list of items from the JSON data
    items = data['items']

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(items)

    # Convert 'lastSeen' to datetime format in Central Time Zone
    central_tz = timezone(s.MY_TIMEZONE)
    df['lastSeen'] = df['lastSeen'].apply(lambda x: parser.isoparse(x).astimezone(central_tz).strftime('%Y-%m-%d %H:%M:%S'))

    # Convert the 'Date' column to datetime
    df['lastSeen'] = pd.to_datetime(df['lastSeen'])

    # Expand the 'arena' column into separate columns
    arena_cols = pd.json_normalize(df['arena'], record_prefix='arena.')
    df = pd.concat([df, arena_cols], axis=1)
    df.drop('arena', axis=1, inplace=True)

    # Create an Excel file
    writer = pd.ExcelWriter(s.WORKBOOK_NAME, engine='xlsxwriter')

    # Write the DataFrame to Excel
    df.to_excel(writer, sheet_name=s.WORKSHEET_NAME, index=False)

    # Get the worksheet object
    workbook = writer.book
    worksheet = writer.sheets[s.WORKSHEET_NAME]

    # Define the date format as Excel-sortable:
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

    # Apply the date format to the 'lastSeen' column
    last_seen_col = df.columns.get_loc('lastSeen')
    worksheet.set_column(last_seen_col, last_seen_col, None, date_format)

    # Save the Excel file
    writer.close()