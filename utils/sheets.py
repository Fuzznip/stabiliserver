import gspread
from oauth2client.service_account import ServiceAccountCredentials
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time
from dotenv import load_dotenv
load_dotenv()
import os

import utils.tile_race as tile_race

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

# firebase_credentials = credentials.Certificate(os.path.abspath(os.environ.get("FIREBASE_CREDENTIALS")))
# firebase_admin.initialize_app(firebase_credentials)
# db = firestore.client()

# lastRefresh is the last time the cache was refreshed, initialize to epoch
lastRefresh = datetime.utcfromtimestamp(0)

trackedItems = []

# dropDictionary is a dictionary of pairs of items and drop sources to the list of channels they should post in
# eg. { ("abyssal whip", "abyssal demon"): [ "1233130963870154864", "1232048319996625029", ... ] }
dropDictionary: dict[tuple[str, str], list[str]] = {}

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

def refresh_cache(force = False):
    global lastRefresh, trackedItems, dropDictionary

    # Check if the cache is older than 1 minute
    if (datetime.utcnow() - lastRefresh).total_seconds() < 60 and not force:
        return
    
    # Clear the tracked items and drop dictionary
    trackedItems = []
    dropDictionary = {}

    # Get data from the first column of the sheet except the first row, lower case it, and store it in trackedItems
    trackedItems = [item.lower() for item in readSheet.col_values(1)[1:]]
    # Get data from the rest of the columns (B, C, D, ...) and store it in inputColumns
    inputColumns = readSheet.get_all_values()
    # Transpose the inputColumns to convert from a list of rows to a list of columns
    inputColumns = list(map(list, zip(*inputColumns)))
    # Remove the first column (the tracked items) from the inputColumns
    inputColumns = inputColumns[1:]

    # For each input column, iterate through the rows and insert the data into the drop dictionary
    for column in inputColumns:
        # Grab the first row of the column to get the output id
        outputId = column[0]
        # Grab the rest of the rows to get the input data
        inputRows: list[str] = column[1:]
        # For each row in the input data, insert it into the drop dictionary
        for row in inputRows:
            # If the row is empty, skip it
            if row == "":
                continue

            # TODO: Parse the row in the format "(-)item:source" 
            # (-) is optional and indicates whether the item should be blacklisted
            # item is the item name
            # source is the source of the drop

            # If the row starts with a "-" character, add the item to the blacklist and skip it


            # Split the row into the item and source
            # If the item has no source, set the source to ""
            if ":" not in row:
                item = row
                source = ""
            else:
                item, source = row.split(":")
            # Lowercase the item and source
            item = item.lower()
            source = source.lower()

            # If the (item, source) pair is not in the drop dictionary, create a new list for it with the output id
            if (item, source) not in dropDictionary:
                dropDictionary[(item, source)] = [outputId]
            # Otherwise, append the output id to the list
            else:
                dropDictionary[(item, source)].append(outputId)
                
    # Update the last refresh time  
    lastRefresh = datetime.utcnow()

def write(player: str, discordId: str, itemSource: str, itemName: str, itemValue: int, itemQuantity: int, submitType: str) -> None:
    data = [ datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), player, discordId, itemSource, itemName, itemValue, itemQuantity, itemValue * itemQuantity, submitType ]
    writeSheet.append_row(data)

    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "player": player,
        "discordId": discordId,
        "itemSource": itemSource,
        "itemName": itemName,
        "itemValue": itemValue,
        "itemQuantity": itemQuantity,
        "totalValue": itemValue * itemQuantity,
        "submitType": submitType
    }

    #db.collection("drops").add(data)

# Return value in the form of a list of tuples of item names to their lists of output ids
def submit(rsn, discordId, source, item, itemPrice, itemQuantity, submitType):
    output = {
        "threadList": [],
    }
    # result = tile_race.parse_tile_race_submission(submitType, rsn, discordId, source, item, itemPrice, itemQuantity)
    # if result is not None:
    #     output["threadList"].append(result["thread_id"])
    #     output["message"] = result["message"]

    refresh_cache()
    # Create a query for the item and source
    query = (item.lower(), source.lower())
    
    # TODO: Check blacklists

    # Check if the query is in the drop dictionary
    if query in dropDictionary:
        for threadId in dropDictionary[query]:
            output["threadList"].append(threadId)
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")
        return output

    # Check if the query is in the drop dictionary without a specific source
    query = (item.lower(), "")
    if query in dropDictionary:
        for threadId in dropDictionary[query]:
            output["threadList"].append(threadId)
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")
        return output
    
    # If the query is not in the drop dictionary, check if the item is in the tracked items
    if item.lower() in trackedItems:
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")

    if item.lower() + ":" + source.lower() in trackedItems:
        write(rsn, discordId, source, item, itemPrice, itemQuantity, submitType)
        print(submitType + ": " + rsn + " - " + item + " (" + source + ")")

    return output
