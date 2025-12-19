import pandas as pd # pandas is used to read csv files and also to run sql queries easily

def migrate_dataset_metadata(conn):
    data = pd.read_csv("DATA/datasets_metadata.csv") # load the metadata from a csv file into a dataframe
    data.to_sql('datasets_metadata', conn, if_exists="append", index=False) # write the dataframe into the database table, append if table already exists
    conn.close() # close the database connection

def get_all_datasets_metadata(conn):
    sql = "SELECT * FROM datasets_metadata" # sql query to select all rows from the metadata table
    data = pd.read_sql(sql, conn) # run the query and load the results into a dataframe
    return data # return the dataframe so it can be used in the app