import bcrypt # bcrypt is imported so passwords can be hashed securely when users are added
import pandas as pd # pandas is imported so I can run sql queries and show results in a dataframe

def add_user(conn, name, hash_passwordTEXT):
    curr = conn.cursor() # make a cursor object so I can run sql commands
    sql = "INSERT INTO users (username, password_hashTEXT) VALUES (?, ?)" # sql command to insert a new user into the users table
    parram = (name, hash_passwordTEXT) # parameters for the sql command, username and hashed password
    curr.execute(sql, parram) # run the sql command with the parameters
    conn.commit() # save the changes to the database

def migrate_users(conn):
    with open("DATA/user.txt", "r") as f: # open the user file in read mode
        users = f.readlines() # read all lines from the file

        for user in users: # loop through each line
            name, hash = user.strip().split(",") # split the line into username and hash
            add_user(conn, name, hash) # add each user into the database
        conn.close() # close the database connection

def get_all_users(conn):
    curr = conn.cursor() # make a cursor object
    sql = "SELECT * from users" # sql command to select all users
    curr.execute(sql) # run the sql command
    users = curr.fetchall() # fetch all rows from the result
    conn.close() # close the database connection
    return(users) # return the list of users

def get_user(conn, name_):
    curr = conn.cursor() # make a cursor object
    sql = "SELECT  * from users WHERE username = ?" # sql command to select a user by username
    param = (name_,) # parameter for the sql command
    curr.execute(sql, param) # run the sql command with the parameter
    user = curr.fetchone() # fetch one row from the result
    return user # return the user

def get_all_users_pandas(conn):
    sql = "SELECT * from datasets_metadata" # sql command to select all rows from datasets_metadata
    data = pd.read_sql(sql, conn) # run the query and load the results into a dataframe
    print(data) # print the dataframe