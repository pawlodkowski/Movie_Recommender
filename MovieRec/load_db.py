
###############
path="C:/Users/Lena/Desktop/DataScience/Goals/Movie_Recommender/data/" 
your_djangoproject_home="C:/Users/Lena/Desktop/DataScience/Goals/Movie_Recommender/MovieRec/"

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='MovieRec.settings'

import django
django.setup()

from mvr.models import Movielens, Links, Tags, Ratings #, Omdb, Ratings
import csv
import re
#####################


with open(str(path + "movies.csv"), encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    for row in reader:
        try:
            _, created = Movielens.objects.get_or_create(
                         movieId=row[0],
                         title=row[1],
                         genres=row[2],
                         year=re.findall("\(([0-9]{4})\)", row[2])
                )
        except:
            _, created = Movielens.objects.get_or_create(
                         movieId=row[0],
                         title=row[1],
                         genres=row[2],
                         year=0
                )

with open(str(path + "links.csv"), encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    for row in reader:
        _, created = Links.objects.get_or_create(
                         movieId=row[0],
                         imdbId=row[1],
                         tmdbId=row[2]
                )

with open(str(path + "tags.csv"), encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    for row in reader:
        _, created = Tags.objects.get_or_create(
                userId = row[0],
                movieId = row[1],
                tag = row[2],
                timestamp = row[3]                
                )

with open(str(path + "ratings.csv"), encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    for row in reader:
        _, created = Ratings.objects.get_or_create(
                userId = row[0],
                movieId = row[1],
                rating = row[2],
                timestamp = row[3]                
                )
