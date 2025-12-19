import sqlite3 # sqlite3 is used to connect to and work with a local sqlite database file

def get_db_connection():
    conn = sqlite3.connect("DATA/intelligence_platform.db") # open a connection to the database file stored in DATA folder
    return conn # return the connection object so other functions can run queries on it