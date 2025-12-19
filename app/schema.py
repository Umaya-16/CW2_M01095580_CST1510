def create_user_table(conn):
    curr = conn.cursor() # make a cursor object so I can run sql commands
    sql = """ CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hashTEXT TEXT NOT NULL) """ # sql command to create a users table if it does not already exist
    curr.execute(sql) # run the sql command
    conn.commit() # save the changes to the database