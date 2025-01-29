import sqlite3

# Path to the database
db_path = "train_booking.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Query the trains table
cursor.execute("SELECT * FROM trains LIMIT 5;")
trains = cursor.fetchall()
print("Trains:", trains)

# Query the seats table
cursor.execute("SELECT * FROM seats LIMIT 5;")
seats = cursor.fetchall()
print("Seats:", seats)

# Close the connection
conn.close()
