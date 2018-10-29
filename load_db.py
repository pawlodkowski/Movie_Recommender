
import pandas as pd
import sqlite3


# reading csv for now... will be replaced by smart delta-handling API connection!
#PATH = "data/OMDB.csv"
#df = pd.read_csv(PATH)

df_omdb = pd.read_csv("data/omdb.csv")
df_movielens = pd.read_csv("data/movies.csv")
df_links = pd.read_csv("data/links.csv")
df_ratings = pd.read_csv("data/ratings.csv")
df_tags = pd.read_csv("data/tags.csv")

# establish connection to database
db = sqlite3.connect('data/movies.db')


def create_db():
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
    
    
    CREATE TABLE IF NOT EXISTS movielens (
        movieId STRING(15),
        title VARCHAR(250),
        genres TEXT
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON movielens(movieId);
    
    
    CREATE TABLE IF NOT EXISTS links (
        movieId STRING(15),
        imdbId STRING(15),
        tmdbId STRING(15)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON links(movieId);   
    
    
    CREATE TABLE IF NOT EXISTS ratings (
        userId STRING(15),
        movieId STRING(15),
        rating FLOAT,
        timestamp STRING(20)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON ratings(movieId);       
    
    
    CREATE TABLE IF NOT EXISTS tags (
        userId STRING(15),
        movieId STRING(15),
        tag TEXT,
        timestamp STRING(20)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS i1 ON tags(movieId);     
    """
    db.executescript(DB_SETUP)


def drop_table(tablename):
    DROP_TABLE = f"DROP TABLE {tablename};"
    db.executescript(DROP_TABLE)
    #db.close()
       
    
def insert_data():
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
       
    for i, row in df_movielens.iterrows():
        query = 'INSERT INTO movielens VALUES (?,?,?)'
        db.execute(query, (row['movieId'], 
                           row["title"], 
                           row["genres"]
                           ))

    for i, row in df_links.iterrows():
        query = 'INSERT INTO links VALUES (?,?,?)'
        db.execute(query, (row["movieId"], 
                           row["imdbId"], 
                           row["tmdbId"]
                           ))

    for i, row in df_ratings.iterrows():
        query = 'INSERT INTO ratings VALUES (?,?,?,?)'
        db.execute(query, (row['userId'], 
                           row["movieId"], 
                           row["rating"],
                           row["timestamp"]                           
                           ))
        
    for i, row in df_tags.iterrows():
        query = 'INSERT INTO tags VALUES (?,?,?,?)'
        db.execute(query, (row['userId'], 
                           row["movieId"], 
                           row["tag"],
                           row["timestamp"]                           
                           ))


########## select what should be done
#create_db()
#drop_table("movies")
#insert_data() 


query = '''SELECT tag, tags.movieId, movielens.title 
        FROM tags 
        INNER JOIN ratings on ratings.movieId = tags.movieId JOIN movielens on movielens.movieId = ratings.movieId 
        WHERE ratings.rating > 4.0
        '''
df_out = pd.read_sql(query, db)
print(df_out.head(10))

#db.commit()
db.close()
