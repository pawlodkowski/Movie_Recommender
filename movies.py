# Imports
import pandas as pd
PATH = "reviews.xlsx"
df = pd.read_excel(PATH)


print("some words")

genre = input("enter a genre: ")
reviewer = input("your favourite reviewer: ")


if genre:
    g = df[df["Genre"] == genre]
else:
    g = df


if g.shape[0] > 0:
    result = g.sort_values(["Rating"], ascending = False)
    print(g.head(3).sample(1))
else:
    print("No result")
#(result.head(3).sample(1))
print(result.head(3).sample(1))