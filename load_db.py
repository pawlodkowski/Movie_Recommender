
import pandas as pd
import sqlite3
import re


# reading csv for now... will be replaced by smart delta-handling API connection!
#PATH = "data/OMDB.csv"
#df = pd.read_csv(PATH)


############################################################################### establish connection to database

db = sqlite3.connect('data/movies.db')

############################################################################### Creating tables  
    
def create_table_omdb():
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS omdb (
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
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON omdb(imdbid);
    """
    db.executescript(DB_SETUP)
    

def create_table_movielens():
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS movielens (
        movieId STRING(15),
        title VARCHAR(250),
        genres TEXT,
        year INTEGER
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON movielens(movieId);"""
    db.executescript(DB_SETUP)
    

def create_table_ratings():
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS ratings (
        userId STRING(15),
        movieId STRING(15),
        rating FLOAT,
        timestamp TEXT
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON ratings(movieId); """  
    db.executescript(DB_SETUP)
    
    
def create_table_links():
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS links (
        movieId STRING(15),
        imdbId STRING(15),
        tmdbId STRING(15)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON links(movieId); """  
    db.executescript(DB_SETUP)    


def create_table_tags():
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS tags (
        userId STRING(15),
        movieId STRING(15),
        tag TEXT,
        timestamp TEXT
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON tags(movieId);  """
    db.executescript(DB_SETUP) 


def create_tables(tablenames):
    if "omdb" in tablenames:
        create_table_omdb()
    if "movielens" in tablenames:
        create_table_movielens()
    if "ratings" in tablenames:
        create_table_ratings()
    if "links" in tablenames:  
        create_table_links()
    if "tags" in tablenames: 
        create_table_tags()


def drop_table(tablenames):
    for i in tablenames:
        DROP_TABLE = f"DROP TABLE {i};"
        db.executescript(DROP_TABLE)
    #db.close()

############################################################################### Preparing Data For Insert
# Load Data 
    
df_omdb = pd.read_csv("data/omdb.csv")
df_movielens = pd.read_csv("data/movies.csv")
df_links = pd.read_csv("data/links.csv")
df_ratings = pd.read_csv("data/ratings.csv")
df_tags = pd.read_csv("data/tags.csv")

# Reshape Data

def get_year(x):
    y = re.findall("\(([0-9]{4})\)", x)
    try:
        y = y[0]
    except:
        y = 0
    return y

df_movielens["year"] = df_movielens["title"].apply(get_year)
df_ratings["timestamp"] = pd.to_datetime(df_ratings["timestamp"], unit='s')
df_ratings["timestamp"] = df_ratings["timestamp"].astype(str)
df_tags["timestamp"] = pd.to_datetime(df_tags["timestamp"], unit='s')
df_tags["timestamp"] = df_tags["timestamp"].astype(str)



############################################################################### Insert Data

def insert_data(tablenames):
    if "omdb" in tablenames:
        for i, row in df_omdb.iterrows():
            query = 'INSERT INTO omdb VALUES (?,?,?,?,?,?,?,?,?,?)'
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
 
    if "movielens" in tablenames: 
        for i, row in df_movielens.iterrows():
            query = 'INSERT INTO movielens VALUES (?,?,?,?)'
            db.execute(query, (row['movieId'], 
                               row["title"], 
                               row["genres"],
                               row["year"]
                               ))

    if "links" in tablenames: 
        for i, row in df_links.iterrows():
            query = 'INSERT INTO links VALUES (?,?,?)'
            db.execute(query, (row["movieId"], 
                               row["imdbId"], 
                               row["tmdbId"]
                               ))

    if "ratings" in tablenames: 
        for i, row in df_ratings.iterrows():
            query = 'INSERT INTO ratings VALUES (?,?,?,?)'
            db.execute(query, (row['userId'], 
                               row["movieId"], 
                               row["rating"],
                               row["timestamp"]                           
                               ))

    if "tags" in tablenames:  
        for i, row in df_tags.iterrows():
            query = 'INSERT INTO tags VALUES (?,?,?,?)'
            db.execute(query, (row['userId'], 
                               row["movieId"], 
                               row["tag"],
                               row["timestamp"]                           
                               ))


############################################################################### select what to do

tablenames = ["omdb", "movielens", "tags", "links", "ratings"] 
#drop_table(tablenames)
create_tables(tablenames)
insert_data(tablenames) 


#query = '''SELECT timestamp FROM tags'''
#df_out = pd.read_sql(query, db)
#print(df_out.head(10))

#print(df_tags["timestamp"].head(5))

############################################################################### commit and close
db.commit()
db.close()
