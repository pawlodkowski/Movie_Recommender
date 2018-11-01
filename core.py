import sqlite3
import pickle
import pandas as pd
import numpy as np
from more_itertools import unique_everseen
from sklearn.metrics.pairwise import cosine_similarity


def get_data_from_db(database_directory, tablename):
    db = sqlite3.connect(database_directory)
    query = f"SELECT * FROM {tablename}"
    df = pd.read_sql(query, db)
    db.close()
    return df


def get_all_movie_ids(database_directory, tablename = "ratings"):
    d0 = get_data_from_db(database_directory, tablename)
    all_movie_ids = sorted(set(d0["movieId"]))
    return all_movie_ids


def create_users_vs_movies_matrix(df):
    df = df.drop("timestamp", axis = 1)
    df = df.set_index(["userId", "movieId"])
    df = df.unstack()
    df = df.fillna(0)
    return df


def load_NMF_model(NMF_model_directory):
    loaded_model = pickle.load(open(NMF_model_directory, "rb"))
    return loaded_model
        

def apply_NMF(trained_model, converted_user_input, filtered_movie_ids, all_movie_ids, n_results):
    
    # preparing P and Q
    P = trained_model.components_
    user_Q = trained_model.transform([converted_user_input])
    
    # creating new R, = list of NMF_scores for particular user
    user_R = np.dot(user_Q, P)
    recommendations_user = list(user_R[0])
    
    # labelling NMF_scores with movie ids
    recommendations_with_movie_id = dict(zip(all_movie_ids, recommendations_user))
    
    # applying filters
    recommendations_with_movie_id_filtered = list([[x,recommendations_with_movie_id[x]] for x in filtered_movie_ids])
    results = pd.DataFrame(recommendations_with_movie_id_filtered, columns = ["movieId", "NMF_score"])
    results = results.sort_values(by = "NMF_score", ascending = False)
    output = list(results["movieId"])
    return output


def apply_CF(converted_user_input, all_movie_ids, users_vs_movies_matrix, filtered_movie_ids):
    
    def make_cosine_heatmap(df):
        labels = list(df.index.values) 
        cosine_similarities = cosine_similarity(df)
        results_df = pd.DataFrame(cosine_similarities, columns = labels, index = labels)
        return results_df

    def get_similar_users(cosine_heatmap, userId):
        results_for_one_user = cosine_heatmap.loc[userId].sort_values(ascending = False) # get similar users
        similar_users = list(results_for_one_user.keys())[1:]
        return similar_users
    
    #create user row in dataframe
    user_input_df_row = pd.DataFrame(converted_user_input, index = all_movie_ids).transpose()
    user_input_df_row
    
    # add that user row into existing df
    users_vs_movies_matrix_complemented = users_vs_movies_matrix.copy()
    users_vs_movies_matrix_complemented.loc[0] = converted_user_input
    
    # determine ordered list of similar users via cosine similarity
    cosine_heatmap = make_cosine_heatmap(users_vs_movies_matrix_complemented)
    similar_users = get_similar_users(cosine_heatmap, 0)
    
    # apply filters
    filtered_uvmm_complemented =  users_vs_movies_matrix_complemented["rating"][filtered_movie_ids]
    
    # go through every similar user, starting from most similar one, check for conditions below and append movieId to list
    recommended_movie_ids = []
    for user in similar_users:
        checking_movies = ((filtered_uvmm_complemented.loc[0] == 0.0) & (filtered_uvmm_complemented.loc[user] >= 5.0))
        d = dict(checking_movies)
        recommended_movie_ids_from_user = list(filter(d.get, d)) #returning keys (movieids) from dict where value is True
        recommended_movie_ids += recommended_movie_ids_from_user
        recommended_movie_ids = list(unique_everseen(recommended_movie_ids)) # delete duplicates from list keeping their order 
        if len(recommended_movie_ids) >= 20:
            break
    return recommended_movie_ids


def convert_filters(filters):
    #takes a list of filter strings and return list of movie ids matching filter criteria
    return filtered_moviedids


def convert_input():
    # takes tuples from django website and turns them into readable input for NMF etc.
    return converted_input


def make_final_recommendations(recoms_NMF, recoms_CF):
    # create function that merges the results of NMF and collaborative filtering
    return final_recommendations
    

def convert_to_imdbid(movieids):
    # converts list of movieids into list of imdb ids
    return imdbids


def make_poster_links(imdbids):
    # return a list of posterlinks according to the imdbids
    return poster_links
    
    
def recommender(website_user_ratings, website_filters):
    
    database_directory = "data/movies.db"
    NMF_model_directory = "data/trained_NMF_model.sav"
    #d0 = get_data_from_db(database_directory, "ratings")

    users_vs_movies_matrix = create_users_vs_movies_matrix(d0)
    
    filtered_movie_ids = convert_filters(website_filters)
    converted_user_input = convert_input(website_user_ratings)
    all_movie_ids = get_all_movie_ids(database_directory, tablename = "ratings")
    trained_model = load_NMF_model(NMF_model_directory)
    n_models = 10
    
    NMF_results = apply_NMF(trained_model, converted_user_input, filtered_movie_ids, all_movie_ids, n_results)
    CF_results = apply_CF(converted_user_input, all_movie_ids, users_vs_movies_matrix, filtered_movie_ids)
    
    final_recommendations = make_final_recommendations(NMF_results, CF_results)
    
    # map to imbdid
    # make poster links
    
    return final_recommendations

