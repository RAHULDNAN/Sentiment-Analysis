#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import random
from bs4 import BeautifulSoup


# In[23]:


response = requests.get('https://www.yelp.com/biz/abc-kitchen-new-york')
text = BeautifulSoup(response.text, 'html.parser')


# In[26]:


import re
num_reviews = text.find('span', attrs = {'class':  'css-1fdy0l5'}).string
num_reviews = int(re.findall('\d+', num_reviews)[0])
print(num_reviews)


# In[27]:


url_list = []
for i in range(0, num_reviews, 10):
    url_list.append('https://www.yelp.com/biz/abc-kitchen-new-york?start=' +str(i))


# In[28]:


reviews = text.find_all('div', attrs = {'class': 'review__09f24__oHr9V border-color--default__09f24__NPAKY'})
print(len(reviews))


# In[29]:


#Username
review = reviews[0]
username = review.find('a', attrs = {'class': 'css-1m051bw'}).string
print(username)


# In[30]:


#Location
location = review.find('span', attrs = {'class': 'css-qgunke'}).get_text()
print(location)


# In[31]:


#Rating
rating = review.find('div', attrs = {'class': 'five-stars__09f24__mBKym five-stars--regular__09f24__DgBNj display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY'})
#rating = float(re.findall('\d+', rating)[0])
print(rating['aria-label'])


# In[32]:


#Date
date = review.find('span', attrs = {'class': 'css-chan6m'}).get_text()
print(date)


# In[33]:


#Content
content = review.find('p').get_text()
print(content)


# In[34]:


import csv


# In[35]:


with open('reviews.csv', 'w', encoding = 'utf-8', newline = '') as csvfile:
    review_writer = csv.writer(csvfile)
    for review in reviews:
        dic = {}
        username = review.find('a', attrs = {'class': 'css-1m051bw'}).string
        location = review.find('span', attrs = {'class': 'css-qgunke'}).get_text()
        date = review.find('span', attrs = {'class': 'css-chan6m'}).get_text()
        rating = review.find('div', attrs = {'class': 'five-stars__09f24__mBKym five-stars--regular__09f24__DgBNj display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY'})
        #rating = float(re.findall('\d+', rating)[0])
        content = review.find('p').get_text()
        dic['username'] = username
        dic['location'] = location
        dic['date'] = date
        dic['rating'] = rating['aria-label']
        dic['content'] = content
        review_writer.writerow(dic.values())
        


# In[36]:


import time
import random

def scrap_single_page(reviewws, csvwriter):
    for review in reviews:
        dic = {}
        username = review.find('a', attrs = {'class': 'css-1m051bw'}).string
        location = review.find('span', attrs = {'class': 'css-qgunke'}).get_text()
        date = review.find('span', attrs = {'class': 'css-chan6m'}).get_text()
        rating = review.find('div', attrs = {'class': 'five-stars__09f24__mBKym five-stars--regular__09f24__DgBNj display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY'})
        #rating = float(re.findall('\d+', rating)[0])
        content = review.find('p').get_text()
        dic['username'] = username
        dic['location'] = location
        dic['date'] = date
        dic['rating'] = rating['aria-label']
        dic['content'] = content
        review_writer.writerow(dic.values())
        
with open('reviews.csv', 'w', encoding = 'utf-8', newline = '') as csvfile:
    review_writer = csv.writer(csvfile)
    for index, url in enumerate(url_list):
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        reviews = soup.find_all('div', attrs = {'class': 'review__09f24__oHr9V border-color--default__09f24__NPAKY'})
        scrap_single_page(reviews, review_writer)
        time.sleep(random.randint(1,3))
        print('Finished page ' + str(index + 1))

