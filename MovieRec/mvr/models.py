from django.db import models

# Create your models here.
class Omdb(models.Model):
    imdbid = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    pgr = models.CharField(max_length=10)
    runtime = models.IntegerField()
    genre = models.CharField(max_length=20)
    keywords = models.TextField()
    rating = models.DecimalField(max_digits=4, decimal_places=1)
    nvoters = models.IntegerField()
    wrating = models.DecimalField(max_digits=10, decimal_places=2)
    
class Movielens(models.Model):
    movieId = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=200)
    genres = models.TextField()
    year = models.IntegerField()
    
class Ratings(models.Model):
    userId = models.CharField(max_length=15)
    movieId = models.CharField(max_length=15)
    rating = models.DecimalField(max_digits=4, decimal_places=1)
    timestamp = models.CharField(max_length=20)
    
class Links(models.Model):
    movieId = models.CharField(max_length=15, unique=True)
    imdbId = models.CharField(max_length=15)
    tmdbId = models.CharField(max_length=15)
    
class Tags(models.Model):
    userId = models.CharField(max_length=15)
    movieId = models.CharField(max_length=15)
    tag = models.TextField()
    timestamp = models.CharField(max_length=20)