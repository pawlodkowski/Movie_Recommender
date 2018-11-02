###############################################################################
''' 
Spicy Movie Recommender 5000


# todo
# apply superior filtering algorithm
# magic merger returns duplicates sometimes...
# prepare data for sending it to the website --> convert to IMDB Ids
'''
############################################################################### Imports

import sqlite3
import pickle
import pandas as pd
import numpy as np
from more_itertools import unique_everseen
from sklearn.metrics.pairwise import cosine_similarity

############################################################################### Functions

def get_data_from_db(database_directory, tablename):
    db = sqlite3.connect(database_directory)
    query = f"SELECT * FROM {tablename}"
    df = pd.read_sql(query, db)
    db.close()
    return df


def get_all_movie_ids(database_directory, tablename = "mvr_ratings"):
    d0 = get_data_from_db(database_directory, tablename)
    all_movie_ids = sorted(set(d0["movieId"]))
    return all_movie_ids


def create_users_vs_movies_matrix(df):
    df = df.drop("timestamp", axis = 1)
    df = df.drop("id", axis = 1)
    df = df.set_index(["userId", "movieId"])
    df = df.unstack()
    df = df.fillna(0)
    return df


def load_NMF_model(NMF_model_directory):
    loaded_model = pickle.load(open(NMF_model_directory, "rb"))
    return loaded_model


def apply_NMF(trained_model, converted_user_input, filtered_movie_ids, all_movie_ids):

    # preparing P and Q
    P = trained_model.components_
    user_Q = trained_model.transform([converted_user_input])

    # creating new R, = list of NMF_scores for particular user
    user_R = np.dot(user_Q, P)
    NMF_scores_user = list(user_R[0])

    # labelling NMF_scores with movie ids
    recommendations_with_movie_id = dict(zip(all_movie_ids, NMF_scores_user))

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
    #user_input_df_row = pd.DataFrame(converted_user_input, index = all_movie_ids).transpose()

    # add that user row into existing df
    users_vs_movies_matrix_complemented = users_vs_movies_matrix.copy()
    users_vs_movies_matrix_complemented.loc[0] = converted_user_input#user_input_df_row

    # determine ordered list of similar users via cosine similarity
    cosine_heatmap = make_cosine_heatmap(users_vs_movies_matrix_complemented)
    similar_users = get_similar_users(cosine_heatmap, 0)

    # apply filters
    filtered_uvmm_complemented =  users_vs_movies_matrix_complemented["rating"][filtered_movie_ids]

    # go through every similar user, starting from most similar one, check for conditions below and append movieId to list
    recommended_movie_ids = []
    for user in similar_users:
        checking_movies = ((filtered_uvmm_complemented.loc[0] == 0.0) & (filtered_uvmm_complemented.loc[user] == 5.0))
        d = dict(checking_movies)
        recommended_movie_ids_from_user = list(filter(d.get, d)) #returning keys (movieids) from dict where value is True
        recommended_movie_ids += recommended_movie_ids_from_user
        recommended_movie_ids = list(unique_everseen(recommended_movie_ids)) # delete duplicates from list keeping their order
        if len(recommended_movie_ids) >= 30:
            break
    return recommended_movie_ids

def apply_filtering(website_filters, database_directory):
    
    def splitter1(x):
        return ",".join(x.split("|")).lower()
    def splitter2(x):
        return ",".join(x.split(",")).lower()
    def splitter3(x):
        return x.split(",")
    
    # make searchable extract: keywords vs movieIds
    # load data
    dm = get_data_from_db(database_directory, "mvr_movielens")
    dt = get_data_from_db(database_directory, "mvr_tags")
    # make genres to a string
    dm["genres"] = dm["genres"].apply(splitter1)
    # group tags per movieid and make string out of it
    dt = dt.groupby(["movieId"])['tag'].apply(lambda x: ','.join(x)).reset_index()
    dt["tag"] = dt["tag"].apply(splitter2)
    # merge combined tags on dm
    df = pd.merge(dm, dt, how = "left", on = "movieId")
    df["tag"].fillna(value = "", inplace = True)
    # keyword column
    df["keywords"] = df["genres"] + df["tag"]  + df["title"]
    # make extact for searching
    keywords = list(df["keywords"])
    movieIds = list(df["movieId"])
    keywords_and_movieids = list(zip(keywords, movieIds))
    
    #get results
    filters = website_filters.lower().replace(",", " ").split(" ")
    
    raw = website_filters.lower().replace(",", " ").strip().split(" ")
    while '' in raw:
        raw.remove('')
    
    filtered_ids = []
    for i, movie in enumerate(keywords_and_movieids):
        found = []
        for keyword in filters:
            if keyword.lower() in keywords_and_movieids[i][0]:
                found.append(True)
            else:
                found.append(False)
        if all(found):
            filtered_ids.append(keywords_and_movieids[i][1])
        else:
            continue
    filtered_ids = sorted(list(set(filtered_ids)))
    
    return filtered_ids
        
    

def movieIds_by_genre(desired_genre, database_directory):

    db = sqlite3.connect(database_directory)
    query = '''SELECT title, genres, mvr_ratings.*, mvr_tags.tag, mvr_tags.timestamp AS ts
           FROM mvr_movielens
           JOIN mvr_ratings ON mvr_movielens.movieId = mvr_ratings.movieId
           LEFT JOIN mvr_tags ON mvr_movielens.movieID = mvr_tags.movieID AND mvr_ratings.userId = mvr_tags.userId'''
    
    dataframe = pd.read_sql(query, db)
    db.close()
    
    
    genres = list(dataframe['genres'].unique())

    genres_split = []
    for g in genres:
        sublist = g.split('|')
        genres_split.append(sublist)

    flat_list = [item for sublist in genres_split for item in sublist]

    def unique_list(list):
        a = []
        for b in list:
            if b not in a:
                a.append(b)
        return a

    unique_genres = unique_list(flat_list)

    for g in unique_genres:

        col_to_add = []
        for i in list(dataframe['genres']):
            if g in i:
                col_to_add.append(1)
            else:
                col_to_add.append(0)

        dataframe['Genre_{}'.format(g)] = col_to_add

#     del dataframe['genres']
#     #optional

    ids = dataframe['movieId']
    bools = dataframe['Genre_{}'.format(desired_genre)].values
    z = list(zip(ids, bools))
    list_movies = []
    for pair in z:
        if pair[1] == 1:
            list_movies.append(pair[0])

    return unique_list(list_movies)


def translator_dictionary(database_directory):

    db = sqlite3.connect(database_directory)
    query = "SELECT movieId, imdbId FROM mvr_links"
    df_translator = pd.read_sql(query, db)
    movie_IDs = list(df_translator['movieId'])
    IMDB_IDs = list(df_translator['imdbId'])

    #ML_2_IMDB = dict(zip(movie_IDs, IMDB_IDs))
    IMDB_2_ML = dict(zip(IMDB_IDs, movie_IDs))
    db.close()

    return IMDB_2_ML


def convert_django(dataframe, django_data, database_directory):

    new_user_row = pd.DataFrame(np.zeros(shape=(1,len(dataframe.columns))),
                              columns=dataframe.columns)

    dfs_to_concat = [dataframe, new_user_row]
    combined = pd.concat(dfs_to_concat)

    translator = translator_dictionary(database_directory)

    #Assuming that data coming from Django interface is a list of tuples
    for pair in django_data:
        movieId = translator[pair[0]]
        combined.loc[0,("rating", movieId)] = pair[1]
        #where 0 represents userId = 0, aka the new user

    return list(combined.loc[0])


def convert_ids_to_titles(id_list,database_directory):
    
    db = sqlite3.connect(database_directory)
    query = "SELECT movieId, title FROM mvr_movielens"
    df_translator = pd.read_sql(query, db)
    movie_IDs = list(df_translator['movieId'])
    titles = list(df_translator['title'])

    id_2_title = dict(zip(movie_IDs, titles))

    titles = []
    for i in id_list:
        titles.append(id_2_title[i])
    
    db.close()
    return titles

def back_2_IMDB(id_list, database_directory):
    
    db = sqlite3.connect(database_directory)
    query = "SELECT movieId, imdbId FROM mvr_links"
    df_translator = pd.read_sql(query, db)
    movie_IDs = list(df_translator['movieId'])
    IMDB_IDs = list(df_translator['imdbId'])
    
    ML_2_IMDB = dict(zip(movie_IDs, IMDB_IDs))
    
    converted_ids = []
    for i in id_list:
        converted_ids.append(ML_2_IMDB[i])
    
    db.close()
    
    return converted_ids

def magic_merging(NMF, CF):
    # create function that merges the results of NMF and collaborative filtering
    if len(CF) > 20:
        NMF_reduced = NMF[:len(CF)]
        overlap = [x for i,x in enumerate(NMF_reduced) if NMF_reduced[i] in CF]
        if len(overlap) < 10:
            result = NMF[:5]+CF[:5]
        else:
            result = overlap[:10]
    else:
        result = NMF[:10]
    return result


#def convert_to_imdbid(movieids):
    # converts list of movieids into list of imdb ids
#    return imdbids


#def make_poster_links(imdbids):
    # return a list of posterlinks according to the imdbids
#    return poster_links



############################################################################### main function

def recommender(website_user_ratings, website_filters):

    #database_directory = "data/movies.db"
    #database_directory = "../movies.sqlite3"
    database_directory = "C:/Users/Lena/Desktop/DataScience/Goals/Movie_Recommender/MovieRec/movies.sqlite3"
    #NMF_model_directory = "data/NMF_model_trained.sav"
    NMF_model_directory = "C:/Users/Lena/Desktop/DataScience/Goals/Movie_Recommender/data/NMF_model_trained.sav"

    d0 = get_data_from_db(database_directory, "mvr_ratings")
    users_vs_movies_matrix = create_users_vs_movies_matrix(d0)

    converted_user_input = convert_django(users_vs_movies_matrix, website_user_ratings, database_directory)
    #filtered_movie_ids = movieIds_by_genre(website_filters, database_directory)
    filtered_movie_ids = apply_filtering(website_filters, database_directory)

    all_movie_ids = get_all_movie_ids(database_directory, tablename = "mvr_ratings")
    trained_model = load_NMF_model(NMF_model_directory)
    
    if len(filtered_movie_ids) == 0:
        filtered_movie_ids = all_movie_ids
    
    #filtered_movie_ids = all_movie_ids

    NMF_results = apply_NMF(trained_model, converted_user_input, filtered_movie_ids, all_movie_ids)
    #CF_results = apply_CF(converted_user_input, all_movie_ids, users_vs_movies_matrix, filtered_movie_ids)

    #magic_recoms = magic_merging(NMF_results, CF_results)
    magic_recoms = NMF_results
    
    recommended_movie_titles = back_2_IMDB(magic_recoms, database_directory)
    # map to imbdid
    # make poster links

    return recommended_movie_titles[:10]
    #return len(converted_user_input)

#website_user_ratings = [('0092991', 5.0)]
#website_filters = "hanks"

#print(recommender(website_user_ratings, website_filters))
#test = (recommender(website_user_ratings, website_filters))
#test