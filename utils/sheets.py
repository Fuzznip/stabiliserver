import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
from dotenv import load_dotenv
from thefuzz import process, fuzz
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
# lastRefresh is the last time the cache was refreshed, initialize to epoch
lastRefresh = datetime.utcfromtimestamp(0)
itemList = []
specificMonsterItemList = []
trackedItemList = []
specificMonsterTrackedItemList = []
submittedItemList = []
specificMonsterSubmittedItemList = []

thread_id_list = []

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

def submit(player: str, discordId: str, itemSource: str, itemName: str, itemValue: int, itemQuantity: int, type: str) -> None:
  data = [ datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), player, discordId, itemSource, itemName, itemValue, itemQuantity, itemValue * itemQuantity, type ]
  writeSheet.append_row(data)

def refresh_cache():
  global itemList, trackedItemList, submittedItemList, specificMonsterItemList, specificMonsterSubmittedItemList, specificMonsterTrackedItemList, thread_id_list, lastRefresh
  
  # Check if the cache is older than 1 minute
  if (datetime.utcnow() - lastRefresh).total_seconds() < 60:
    return
  
  # Get data from first 2 columns, minus the header
  data = readSheet.batch_get(["A2:A", "B2:B", "C2:C"])
  # Put the data from first column into trackedItemList
  trackedItemList = [item[0] for item in data[0] if item[0] != ""]

  # If the data has a colon in it, it's a specific monster tracked item
  # eg. "abyssal whip:abyssal demon"
  # into an array of objects like this: { "item": "abyssal whip", "monster": "abyssal demon" }
  # then lowercase the item and monster
  specificMonsterTrackedItemList = [item.split(":") for item in trackedItemList if ":" in item]
  specificMonsterTrackedItemList = [ { "item": item[0].lower(), "monster": item[1].lower() } for item in specificMonsterTrackedItemList ]
  # remove items with a colon in it
  trackedItemList = [item.lower() for item in trackedItemList if ":" not in item]

  # Put the data from second column into submittedItemList
  submittedItemList = [item[0] for item in data[1] if item[0] != ""]
  # If the data has a colon in it, it's a specific monster submitted item
  # eg. "abyssal whip:abyssal demon"
  specificMonsterSubmittedItemList = [item.split(":") for item in submittedItemList if ":" in item]
  specificMonsterSubmittedItemList = [ { "item": item[0].lower(), "monster": item[1].lower() } for item in specificMonsterSubmittedItemList ]
  # remove items with a colon in it
  submittedItemList = [item.lower() for item in submittedItemList if ":" not in item]

  # Combine the two lists and remove duplicates
  itemList = list(set(trackedItemList + submittedItemList))
  # For each "item" in the specific monster tracked item list, if the "item" is not in the item list, add it to the item list
  for item in specificMonsterTrackedItemList:
    # add the item to the specific monster item list if it's not already in the item list
    q = { "item": item["item"], "monster": item["monster"] }
    if q not in specificMonsterItemList:
      specificMonsterItemList.append(q)

  for item in specificMonsterSubmittedItemList:
    # add the item to the specific monster item list if it's not already in the item list
    q = { "item": item["item"], "monster": item["monster"] }
    if q not in specificMonsterItemList:
      specificMonsterItemList.append(q)

  # Grab the items from third column and put them into thread_id_list
  thread_id_list = [item[0] for item in data[2] if item[0] != ""]

  # Update the last refresh time  
  lastRefresh = datetime.utcnow()


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

def should_submit(query: str, source: str):
  global specificMonsterItemList
  global itemList

  refresh_cache() # TODO: Make this run once every 5 minutes or something

  # Create object of query and source
  query = query.lower()
  source = source.lower()
  q = { "item": query, "monster": source }

  # Check if the query is in the specific monster item list by fuzzy matching "item" and "monster"
  for item in specificMonsterItemList:
    itemResult = fuzz.ratio(q["item"], item["item"]) > 90
    monsterResult = fuzz.ratio(q["monster"], item["monster"]) > 90
    if itemResult and monsterResult:
      return True
    
  # if the query is not in the specific monster item list, check if the query is in the item list
  return fuzzy_find(query, itemList)

def should_submit_screenshot(query: str, source: str):
  global specificMonsterSubmittedItemList
  global submittedItemList

  # Create object of query and source
  query = query.lower()
  source = source.lower()
  q = { "item": query, "monster": source }

  # Check if the query is in the specific monster item list by fuzzy matching "item" and "monster"
  for item in specificMonsterSubmittedItemList:
    itemResult = fuzz.ratio(q["item"], item["item"]) > 90
    monsterResult = fuzz.ratio(q["monster"], item["monster"]) > 90
    if itemResult and monsterResult:
      return True
    
  # if the query is not in the specific monster item list, check if the query is in the item list
  return fuzzy_find(query, submittedItemList)

def get_thread_id_list():
  global thread_id_list
  return thread_id_list
