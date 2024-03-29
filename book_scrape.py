import requests
from bs4 import BeautifulSoup
import statistics
import re
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import json

page = requests.get("https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century")
soup = BeautifulSoup(page.content, 'html.parser')

book_variances = {}

def find_stars(tag):
    rating = 0
    for each_star in tag.find_all(class_="staticStar p10"):
        rating +=1
    return rating

def ratings_class_match(name):
    if(name.strip().lower()=="staticStars notranslate"):
        return True
    else:
        return False

def get_book_data(url):
    print("currently parsing url" + str(url))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    book_ratings = []
    for each_tag in soup.find_all(class_="staticStars notranslate"):
        book_ratings.append(find_stars(each_tag))
    return book_ratings

for each_tag in soup.find_all(class_="js-tooltipTrigger tooltipTrigger"):
    url_ext = each_tag.a.attrs['href']
    try:
        book_name = url_ext.split(".")[1]
    except:
        book_name = url_ext.replace("https://www.goodreads.com/book/show/", "")
    variance_of_book = get_book_data("https://www.goodreads.com" + str(url_ext))
    book_variances.update({book_name: variance_of_book})

book_std = {}
for key, val in book_variances.items():
    if(len(val)>1):
        book_std.update({key: statistics.pstdev(val)})

book_plt = sorted(book_std.items(), key=lambda x: x[1])

books = {}
for book in book_plt:
    books.update({book[0]: book[1]})

#if results file is not cloned, code to create it.
with open('book_results.json', 'w') as fp:
    json.dump(books, fp)