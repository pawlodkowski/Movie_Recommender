# Imports
import pandas as pd

def get_data():
    # function that returns a dataframe containing movie recommendations
    PATH = "reviews.xlsx"
    df = pd.read_excel(PATH)
    return df

df = get_data()

print("Welcome to the best movie recommender on this planet.")

genre = input("enter a genre (or leave it blank): ")
#reviewer = input("your favourite reviewer: ")


if genre:
    g = df[df["Genre"] == genre]
else:
    g = df


if g.shape[0] > 0:
    result = g.sort_values(["Rating"], ascending = False)

    #(result.head(3).sample(1))
    print(result.head(3).sample(1))
else:
    print("Sorry, no results! No movies in the {} genre.".format(genre))

