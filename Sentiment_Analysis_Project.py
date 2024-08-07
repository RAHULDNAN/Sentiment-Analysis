#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np


# In[53]:


data = pd.read_excel("Restaurant-Reviews.xlsx",na_filter=False)
data


# In[54]:


data['Review1'] = data[data.columns[0:]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
data


# In[55]:


data['Liked1'] = data['Review1'].str.split().str[-1]
data


# In[56]:


data['Review1']=data['Review1'].str.replace('1','')
data


# In[57]:


data['Review1']=data['Review1'].str.replace('0','')
data


# In[58]:


data1 = data.drop(['Review','Liked','Unnamed: 2','Unnamed: 3','Unnamed: 4','Unnamed: 5'], axis=1)
data1


# In[59]:


set(data1['Liked1'])


# In[60]:


data1.columns = ['Review','Liked']


# In[61]:


data1


# In[62]:


colnames=['Username', 'Location', 'Date', 'Rating', 'Reviews'] 


# In[63]:


data2 = pd.read_csv("reviews.csv", names=colnames, header=None)
data2


# In[64]:


data2 = data2.drop(['Username', 'Location', 'Date'], axis=1)
data2


# In[65]:


data2['Rating']=data2['Rating'].str.replace('star rating','')
data2


# In[66]:


set(data2['Rating'])


# In[67]:


columns_titles = ["Reviews","Rating"]
data2=data2.reindex(columns=columns_titles)
data2


# In[68]:


data2.replace({"1 ":0, "2 ":0, "3 ": 0,"4 ": 1, "5 ":1}, inplace=True)


# In[69]:


data2


# In[70]:


set(data2['Rating'])


# In[71]:


data2.columns = ['Review','Liked']
data2


# In[72]:


data3 = pd.concat([data1, data2],axis='rows')


# In[73]:


data3


# In[74]:


data3['Liked'] = data3['Liked'].astype('int64')


# In[75]:


data3.info()


# In[76]:


data3.isnull().sum()


# In[77]:


duplicate=data3.duplicated().sum()
duplicate


# In[78]:


data3.drop_duplicates(inplace=True,keep='first')
duplicate=data3.duplicated().sum()
duplicate


# In[79]:


data3.shape


# In[80]:


import seaborn as sns
sns.countplot(data3['Liked'])


# In[81]:


data3[['Liked']].boxplot()


# In[82]:


data3['Liked'].value_counts(normalize=True).plot(kind='pie', autopct="%.1f")


# In[83]:


#"0='Dislike'"
#"1='Like'"
#
#data3['Liked'].replace({1:'Like',0:'Dislike'},inplace=True)
#data3


# In[84]:


from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
import string
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


# In[85]:


import nltk
nltk.download('omw-1.4')


# In[86]:


stop_words=set(stopwords.words('english'))
puctuation=string.punctuation


# In[87]:


def Text_processing(text):
    process_text=[]
    tk=nltk.word_tokenize(text)
    stop_words=set(stopwords.words('english'))
    for i in tk:
        i=i.lower()
        if ((i not in stop_words) & (i not in string.punctuation)):
            la=WordNetLemmatizer()
            i=la.lemmatize(i)
            process_text.append(i)
    return  process_text
            


# In[88]:


data3['Processed_Review']=data3['Review'].apply(Text_processing)


# In[89]:


data3['Processed_Review']=data3['Processed_Review'].apply(lambda x:' '.join(x))
data3


# In[90]:


data3['Processed_Review'] = data3['Processed_Review'].str.replace('[^\w\s]', '')
data3


# In[91]:


Cv=CountVectorizer(stop_words='english',)


# In[92]:


Cv_text=Cv.fit_transform(data3['Processed_Review']).toarray()


# In[93]:


Cv.vocabulary_


# In[94]:


Cv_text


# In[95]:


x_Cv=Cv_text


# In[96]:


y_Cv=data3['Liked']


# In[97]:


x_train_Cv,x_test_Cv,y_train_Cv,y_test_Cv=train_test_split(x_Cv,y_Cv,train_size=0.7,random_state=50)


# In[98]:


from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(x_train_Cv, y_train_Cv)


# In[99]:


y_pred_Cv = classifier.predict(x_test_Cv)


# In[100]:


from sklearn.metrics import accuracy_score
score = accuracy_score(y_test_Cv,y_pred_Cv)
print("Accuracy score is: {}%".format(round(score*100,2)))


# In[101]:


import pickle
pickle.dump(classifier,open('model.pkl','wb'))
pickle.dump(Cv,open("Cv.pkl",'wb'))

