from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from . import models
# Create your views here.
def home(request):
    return render(request,'base.html')


BASE_CRAIGSLIST_URL = 'https://ahmedabad.craigslist.org/search/?query={}'

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data,features='html.parser')
    post_listings = soup.find_all('li',{'class':'result-row'})
    final_postings = []
    for post in post_listings:
        final_postings.append((post.find(class_='result-title').text,post.find('a').get('href')))
    
    stuff_for_frontend = {
        'search':search,
        'final_postings':final_postings,
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)