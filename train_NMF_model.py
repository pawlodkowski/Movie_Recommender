import pandas as pd
import sqlite3
from sklearn.decomposition import NMF
import pickle

database_directory = "data/movies.db"
tablename = "ratings"
n_components = 15
filename = "data/NMF_model_trained.sav"


def get_data_from_db(database_directory, tablename):
    db = sqlite3.connect(database_directory)
    query = f"SELECT * FROM {tablename}"
    df = pd.read_sql(query, db)
    db.close()
    return df

def create_users_vs_movies_matrix(df):
    df = df.drop("timestamp", axis = 1)
    df = df.set_index(["userId", "movieId"])
    df = df.unstack()
    df = df.fillna(0) # default value
    return df

d0 = get_data_from_db(database_directory, tablename)
R = create_users_vs_movies_matrix(d0)
model = NMF(n_components=n_components, init='random', random_state=42)
model.fit(R)

pickle.dump(model, open(filename, 'wb'))