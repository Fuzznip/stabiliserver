import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
doc = client.open("Clan Data")
itemList = []
readSheet = doc.worksheet("Item Whitelist")
writeSheet = doc.worksheet("Drop Log")

def exponential_backoff(func, max_retries = 5, base_delay = 5):
  retries = 0
  while retries < max_retries:
    try:
      result = func()
      return result  # If the operation was successful, return the result
    except Exception as e:
      print(f"Error: {e}")
      retries += 1
      delay = base_delay * 2 ** (retries - 1)
      print(f"Retrying in {delay} seconds...")
      time.sleep(delay)
  raise Exception("Exceeded maximum number of retries")

def in_item_list(value: str) -> bool:
  global itemList
  if not itemList:
    refresh_cache()
  return value in itemList

def submit(player: str, discordId: str, itemName: str, itemValue: int, itemQuantity: int) -> None:
  data = [ datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), player, discordId, itemName, itemValue, itemQuantity, itemValue * itemQuantity ]
  writeSheet.append_row(data)

def refresh_cache():
  # Assuming data should be in column 1 of sheet
  print("Populating item cache")
  global itemList
  itemList = readSheet.col_values(1)
