import pandas as pd # pandas is used to read csv files and also to run sql queries easily

def migrating_cyber_incidents(conn):
    data = pd.read_csv("DATA/cyber_incidents.csv") # load the cyber incidents data from a csv file into a dataframe
    data.to_sql("cyber_incidents", conn) # write the dataframe into the database table called cyber_incidents

def get_all_cyber_incidents(conn):
    sql = "SELECT * FROM cyber_incidents" # sql query to select all rows from the cyber_incidents table
    data = pd.read_sql(sql, conn) # run the query and load the results into a dataframe
    return(data) # return the dataframe so it can be used in the app