""" 
get_clan_stats.py, 6/9/24 
Get Clash Royale clan members list from Supercell API, output an Excel workbook, and post it to a Discord channel.
"""

import settings as s
import fetch_stats as fs
import create_excel as ce
import upload_discord as ud

if __name__ == '__main__':

    # 1. Fetch stats from Clash Royale API:
    data = fs.fetch_stats()
    if data:
        # 2. Create an Excel workbook file from the stats:
        ce.create_excel(data)
        # 3. Post the Excel file to discord and print the result:
        print(ud.upload_discord())
    else:
        print('Failed to fetch stats from Clash Royale API.')