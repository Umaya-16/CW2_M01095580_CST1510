import pandas as pd # pandas is used to read csv files and also to run sql queries easily

def migrating_it_tickets(conn):
    data = pd.read_csv("DATA/it_tickets.csv") # load the it tickets data from a csv file into a dataframe
    data.to_sql("it_tickets", conn) # write the dataframe into the database table called it_tickets