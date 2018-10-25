"""Load all data from the Spreadsheet into a database

- write a separate script for loading the data
- use sqlite3, see: https://github.com/krother/Python3_Package_Examples/
- try loading the data into a DataFrame """


# create database connection
# function that creates table
### 
'''
ImdbId (string, varchar)
Title (string)
Release year (integer)
pg-rating (string)
runtime (integer)
genre (string) 
keywords (artist, director, writer, plot, language)
imdbrating (float)
weighted rating?
'''
# function that populates table with data from .csv


import pandas as pd
import sqlite3

PATH = "data/OMDB.csv"
df = pd.read_csv(PATH)

db = sqlite3.connect('data/movies.db')

def create_db():
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS movies (
        imdbid STRING(15),
        title VARCHAR(250),
        year INTEGER,
        pgr STRING(10),
        runtime INTEGER,
        genre STRING(250),
        keywords TEXT,
        rating FLOAT,
        nvoters FLOAT,
        wrating FLOAT
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON movies(imdbid);
    """
    db.executescript(DB_SETUP)

def drop_table(tablename):
    DROP_TABLE = f"DROP TABLE {tablename};"
    db.executescript(DROP_TABLE)
    #db.close()
    
    
def insert_data():
    for i, row in df.iterrows():
        query = 'INSERT INTO movies VALUES (?,?,?,?,?,?,?,?,?,?)'
        db.execute(query, (row['imdbID'], 
                           row["Title"], 
                           row["Year"], 
                           row["Rated"], 
                           row["Runtime"], 
                           row["Genre"], 
                           row["Director"] + " " + row["Actors"] + " " + row["Plot"] + " " + row["Language"], 
                           row["imdbRating"], 
                           row["imdbVotes"], 
                           0.0)) # wrating needs numerical values for calculation, imdbVotes is still string

create_db()
#drop_table("movies")
insert_data()



result = db.execute("SELECT title FROM movies")
#print(list(result))


query = "SELECT keywords, wrating FROM movies"
df_out = pd.read_sql(query, db)
print(df_out.head(1))

db.close()
