from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np 
import csv
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

titles = []
authors = []
articles = []
labels = []

def Scrap_data():

    page = requests.get("https://www.bbc.com/news/coronavirus")
    soup = BeautifulSoup(page.content, 'html.parser')

    final_links = []
    articles_links = [] 

    container = soup.find_all("div",{"class":"gel-1/3@xxl"})

    for i in range(len(container)):
        articles_links.append(container[i].a['href'])

    for i in range(len(articles_links)):
        if articles_links[i] in final_links: 
            None
        else:
            final_links.append(articles_links[i])     

    #Prehľadávanie linkov na nové články     
    for item in final_links: 
        page = requests.get(f"https://www.bbc.com{item}")
        soup = BeautifulSoup(page.content, 'html.parser')
        #SCRAP title ↓
        titles.append(soup.find('h1').text)
        #SCRAP author ↓
        try:
            author = soup.find('strong').text
            author = author.replace('By','').lstrip()
            authors.append(author)
        except: 
            author = ""
            authors.append(author)
        #SCRAP text ↓
        text = soup.find_all('div', {'class':'e1xue1i83'})
        article_text = ''
        for i in range(len(text)):
            try: 
                article_text = article_text + text[i].find('p').text
            except: 
                None
        articles.append(article_text)


Scrap_data()
# titles = [] -> all arrays are now filled
# authors = []
# articles = []
# labels = []


#Load the Model back from file
with open("FakeNews_Model.pkl", 'rb') as file:  
    Fake_News_Model = pickle.load(file)

#Load the Model back from file
tfidf_vectorizer = pickle.load(open("tfidf.pickle", "rb"))

def findlabel(newtext):
    vec_text = tfidf_vectorizer.transform([newtext])
    y_pred1 = Fake_News_Model.predict(vec_text)
    return y_pred1[0]

for i in range(len(titles)): 
    text = findlabel(articles[i])
    labels.append(text) 


#Pridanie nových riadkov do dataframu
df = pd.read_csv('train.csv')


with open('train.csv', 'a',encoding='utf-8') as f:
    writer = csv.writer(f)
    df_id = df['id'].iloc[-1]

    for i in range(len(titles)): 
        df_id = df_id + 1
        field=[df_id,titles[i],authors[i],articles[i],labels[i]]
        writer.writerow(field)

df = pd.read_csv('train.csv')

#UPDATE MODEL
def update_model(df): 
    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.80, random_state = 7, shuffle=True)

    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.75)

    vec_train = tfidf_vectorizer.fit_transform(X_train.values.astype('U')) 
    vec_test = tfidf_vectorizer.transform(X_test.values.astype('U'))

    pac = PassiveAggressiveClassifier(max_iter = 50)
    pac.fit(vec_train, y_train)

    Pkl_Filename = "FakeNews_Model.pkl"  
    with open(Pkl_Filename, 'wb') as file:  
        pickle.dump(pac, file)
 
    pickle.dump(tfidf_vectorizer, open("tfidf.pickle", "wb"))
    
    y_pred = pac.predict(vec_test)
    score = accuracy_score(y_test, y_pred)
    print(f'New model is already created with PAC Accurancy: {round(score*100,2)}%')

update_model(df)