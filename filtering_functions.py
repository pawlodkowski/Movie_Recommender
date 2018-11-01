
# coding: utf-8

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# Function 1

# extract the various genres (from the 'genres' column),
# create multiple genre columns out of it,
# then output a list of movies that satisfy requested genre.

def movieIds_by_genre(dataframe, desired_genre):

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

# Function 2

# receive user input data from Django web interface (as a list of tuples),
# use translator dictionary to convert IMDB IDs to movieIds,
# then output a list of the ratings in the correct positions,
# where the rest of the elements in the list (representing all other movies)
# are filled with zeros.

def convert_django(dataframe, django_data):

    new_user_row = pd.DataFrame(np.zeros(shape=(1,len(dataframe.columns))),
                              columns=dataframe.columns)

    dfs_to_concat = [dataframe, new_user_row]
    combined = pd.concat(dfs_to_concat)

    translator = translator_dictionary()

    #Assuming that data coming from Django interface is a list of tuples
    for pair in django_data:
        movieId = translator[pair[0]]
        combined.loc[:,(movieId, 0)] = pair[1]
        #where 0 represents userId = 0, aka the new user

    return list(combined.loc[0])



def translator_dictionary():

    query3 = "SELECT movieId, imdbId FROM links"
    df_translator = pd.read_sql(query3, db)
    movie_IDs = list(df_translator['movieId'])
    IMDB_IDs = list(df_translator['imdbId'])

    ML_2_IMDB = dict(zip(movie_IDs, IMDB_IDs))
    IMDB_2_ML = dict(zip(IMDB_IDs, movie_IDs))

    return IMDB_2_ML
