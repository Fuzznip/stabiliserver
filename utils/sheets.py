import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
from dotenv import load_dotenv
from thefuzz import process
from utils.sqlite_bingo import add_bingo_activity_log
load_dotenv()
import os

# Load credentials from environment variables
credentials_dict = {
  "type": os.environ.get("type"),
  "project_id": os.environ.get("project_id"),
  "private_key_id": os.environ.get("private_key_id"),
  "private_key": os.environ.get("private_key").replace("\\n", "\n"),
  "client_email": os.environ.get("client_email"),
  "client_id": os.environ.get("client_id"),
  "auth_uri": os.environ.get("auth_uri"),
  "token_uri": os.environ.get("token_uri"),
  "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
  "client_x509_cert_url": os.environ.get("client_x509_cert_url")
}

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
doc = client.open("Clan Data")
itemList = []
trackedItemList = []
submittedItemList = []
readSheet = doc.worksheet(os.environ.get("INPUT_SHEET"))
writeSheet = doc.worksheet(os.environ.get("OUTPUT_SHEET"))

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

def add_item_to_list(value: str) -> None:
  global itemList
  refresh_cache()
  itemList.append(value)
  exponential_backoff(lambda: readSheet.append_row([value]))

def in_item_list(value: str) -> bool:
  global itemList
  refresh_cache()
  return value in itemList

def get_item_list():
  return itemList

def is_submitted(value: str) -> bool:
  global submittedItemList
  refresh_cache()
  return fuzzy_find(value, submittedItemList) is not None

def submit(player: str, discordId: str, itemName: str, itemValue: int, itemQuantity: int) -> None:
  data = [ datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), player, discordId, itemName, itemValue, itemQuantity, itemValue * itemQuantity ]
  writeSheet.append_row(data)

  # submit to database
  # add_bingo_activity_log(discordId, itemName, itemValue, itemQuantity)

def refresh_cache():
  global itemList, trackedItemList, submittedItemList
  # Get data from column 1, minus the header
  trackedItemList = readSheet.col_values(1)[1:]
  trackedItemList = [item.lower() for item in trackedItemList]

  # Get data from column 2, minus the header
  submittedItemList = readSheet.col_values(2)[1:]
  submittedItemList = [item.lower() for item in submittedItemList]

  # Combine the two lists and remove duplicates
  itemList = list(set(trackedItemList + submittedItemList))

def fuzzy_find(query: str, itemList: list):
  # Lowercase query
  query = query.lower()
  # Fuzzy find the query in the item list
  results = process.extract(query, itemList, limit = 1)
  # If there is a close match, return the match
  if len(results) > 0 and results[0][1] > 90:
    return results[0]
  # Otherwise, return None
  return None

# Fuzzy check the item list for a given query and return a close match
def fuzzy_find_items(query: str):
  global itemList
  refresh_cache()
  return fuzzy_find(query, itemList)
