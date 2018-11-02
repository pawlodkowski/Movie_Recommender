from django.shortcuts import render

# Create your views here.
#import recommender
#from .mvr import recommender
from .models import Links #meine Tabelle
import requests
import random

#function to get jpg urls
BASE_URL = "http://www.omdbapi.com"
API_KEY = "e20b83a2"
def getjpg(dbid):
    #http://www.omdbapi.com/?i=tt0078908
    params = {'i': dbid, 'apikey': API_KEY}
    r = requests.get(BASE_URL, params=params)
    j = r.json()
    return j['Poster']

# Create your views here.
all_ids = []
def main(request):
    all_movies = random.sample(list(Links.objects.all().values('imdbId')), k=5)
    murl = []
    for i in all_movies:
        imdb = str('tt' + i['imdbId'])
        murl.append(getjpg(imdb)) #links
        all_ids.append(i['imdbId'])
            
    return render(request, "main.html",
                  context={'murl': murl,
                           'allm': all_ids[-5:]
                           })
    
def recm(request):
    #key words
    keyws = request.POST['kws']
    
    #ratings
    resl = []
    for k in all_ids[-5:]:
        resl.append(request.POST[k])  
        
    #test = recommender(list(zip(all_ids[-5:], resl)), keyws)
    test = list(zip(all_ids[-5:], resl))
    
    rurl = []
    for i in test:
        imdb = str('tt' + i[0])
        rurl.append(getjpg(imdb)) #links
        
    
    return render(request, "res.html",
                  context={'rurl': rurl,
                           'keyws': keyws
                          }
                  )
    

