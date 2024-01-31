import sqlite3

# function to set up the database
def setup_bingo_db():
  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Bingos (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, start_time TEXT, end_time TEXT, num_teams INTEGER, link TEXT, description TEXT)")
    conn.commit()

# function to add a bingo to the database
def create_bingo(name, start_time, end_time, num_teams, link, description):
  # make sure table exists
  setup_bingo_db()

  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("INSERT INTO Bingos (name, start_time, end_time, num_teams, link, description) VALUES (?, ?, ?, ?, ?, ?)", (name, start_time, end_time, num_teams, link, description))
    conn.commit()
    # return the bingo's id
    c.execute("SELECT id FROM Bingos WHERE name = ?", (name,))
    return c.fetchone()

# function to delete a bingo from the database
def delete_bingo(id):
  # make sure table exists
  setup_bingo_db()

  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("DELETE FROM Bingos WHERE id = ?", (id,))
    conn.commit()

# function to update a bingo in the database
def update_bingo(id, name, start_time, end_time, num_teams, link, description):
  # make sure table exists
  setup_bingo_db()

  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("UPDATE Bingos SET name = ?, start_time = ?, end_time = ?, num_teams = ?, link = ?, description = ? WHERE id = ?", (name, start_time, end_time, num_teams, link, description, id))
    conn.commit()

# function to get a bingo from the database
def get_bingo(id):
  # make sure table exists
  setup_bingo_db()
  
  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM Bingos WHERE id = ?", (id,))
    return c.fetchone()

# function to get all bingos from the database
def get_all_bingos():
  # make sure table exists
  setup_bingo_db()
  
  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM Bingos")
    return c.fetchall()

# function to get all bingos from the database by name
def get_bingos_by_name(name):
  # make sure table exists
  setup_bingo_db()
  
  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM Bingos WHERE name = ?", (name,))
    return c.fetchall()

# create a bingo activity log table
def create_bingo_activity_log():
  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS BingoActivityLog ( 
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              FOREIGN KEY(bingo_id) REFERENCES Bingos(id), 
              timestamp TEXT, 
              user_name TEXT, 
              user_id INTEGER, 
              team_id INTEGER, 
              item_name TEXT, 
              item_price INTEGER, 
              item_quantity INTEGER, 
              item_total INTEGER)
              """
              )
    conn.commit()

# function to add a bingo activity log to the database
def add_bingo_activity_log(bingo_id, timestamp, user_name, user_id, team_id, item_name, item_price, item_quantity, item_total):
  # make sure table exists
  create_bingo_activity_log()

  with sqlite3.connect('bingo.db') as conn:
    c = conn.cursor()
    c.execute("INSERT INTO BingoActivityLog (bingo_id, timestamp, user_name, user_id, team_id, item_name, item_price, item_quantity, item_total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (bingo_id, timestamp, user_name, user_id, team_id, item_name, item_price, item_quantity, item_total))
    conn.commit()
