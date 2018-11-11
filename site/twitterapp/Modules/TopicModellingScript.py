from __future__ import print_function

from pymongo import MongoClient

import pdb

import json
import re
import datetime
import time

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string

# Importing Gensim
import gensim
from gensim import corpora

import os

import numpy as np

import pandas as pd
from datetime import date
import dateutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3


def topic_modelling(mode):
    """
    mode - str, train or test lda
    
    TODO: figure out why load is not working. currently inspecting methods.
    
    make sure to download nltk dataset
    """
    
    
    client = MongoClient('129.150.114.173', 27017)
    db = client.TwitterStream;
    
    Topics = db["topic"];
    print(Topics);
    
    
    #Get all the Tweets from Database-----------------
    Tweets = [];
    for obj in Topics.find({}):
        Tweets.append(obj);
        
    objects2 = Tweets[:];
    
    print('number of tweets loaded in: {}'.format(len(objects2)))
    
    #Clean the Tweets or Preprocessing--------------------------
    
    tweets_cleaned = [] 
    #tweet_content = db.tweet.find()
    
    #print(u"\U0001F600-\U0001F64F")
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)#emoji_pattern = re.compile('\S')
    hashtag_pattern = re.compile('\#')#('\#\S+[\s|$]')
    mention_pattern = re.compile('\@\S+\s|$')
    #adding the keywords to remove the obivous noice
    bad_words = []
    
    for tweet in Tweets:
    
        tweet['text'] = tweet['text'].lower() #change all the character into lowercase
        tweet['text'] = re.sub(r'http\S+','',tweet['text'])#remove url
        tweet['text'] = mention_pattern.sub(r'',tweet['text'])#remove @username
        #tweet['text'] = re.sub(r'&amp','',tweet['text'])#remove retweet
        #tweet['text'] = hashtag_pattern.sub(r'',tweet['text'])#remove hashtag
        tweet['text'] = emoji_pattern.sub(r'',tweet['text'])#remove emoji
        if not any(bad_word in tweet['text'] for bad_word in bad_words):
            #print(tweet['text'])#remove obivous noice
            tweets_cleaned.append(tweet);
            #if you want to save back into mongodb, define another collection first  
            #print(tweet)
    
    # pdb.set_trace()
        
    #------------------ --------------------
    
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized
    
    doc_clean = [clean(doc['text']).split() for doc in tweets_cleaned]
    
    
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean] 
   
    if mode == 'train':        
        train_lda(doc_term_matrix, dictionary)
        return
    elif mode == 'test': 
        # load existing LDA model 
        Lda = gensim.models.ldamodel.LdaModel
        filename = "lda_model"
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename) 
        # pdb.set_trace()
        ldamodel = Lda.load(path)
    else:
        exit('Error')
   
    #------- Associate each Tweet a Topic by its maximmum probability ------
    
    #get topics for each document
    topics_documents = np.zeros(len(tweets_cleaned))
    
    for i in range(len(objects2)):
        bow = dictionary.doc2bow(tweets_cleaned[i]['text'].split())
        #get the maximmum topic probability of each document
        distribution_topic = ldamodel.get_document_topics(bow);
        topics_documents[i] = distribution_topic.index(max(distribution_topic))
    
    print(topics_documents[1:50]) 
    
    
    #----------- Final Data Wanted ----------
    #Dimensions: Topic - Number of Tweets - Day/Hour
    #data.groupby(['month', 'item'])['date'].count()

    data_frame = pd.DataFrame(tweets_cleaned);
    data_frame['TopicModelled'] = topics_documents;
    #data_frame['created'] = data_frame['created'].apply(datetime.datetime.strptime, args=('%A %B %d %H:%M:%S +0000 %Y',))
    data_frame['created'] = data_frame['created'].apply(dateutil.parser.parse)
    #data_frame['created'] = data_frame['created'].apply(date.strftime("%d/%m/%y"))
    
    #Choose the right grouping of date by
    #%B - Month; %d - day; %H - Hour 
    format_date_group = '%B %d %H';
    aggregated_data = data_frame.groupby([data_frame['created'].dt.strftime(format_date_group), 'TopicModelled'])['TopicModelled'].count();
    
    #----------- Data Frame with all the data needed --------------
    # pdb.set_trace() 
    # ldamodel.show_topic(1)
    # https://radimrehurek.com/gensim/models/ldamodel.html#gensim.models.ldamodel.LdaModel.print_topic
    
    
    
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 17}

    matplotlib.rc('font', **font)
    
    print(aggregated_data)
    dates = aggregated_data.index.levels[0]
    
    #### PLOT frequency against topics
   
    fig = plt.figure(figsize=(20,8)) 
    ax = fig.add_subplot(121)
    filename = "topicmodelling.png"
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    
    for date in aggregated_data.index.levels[0]:
        x = aggregated_data.loc[date].index
        y = aggregated_data.loc[date].values
        ax.plot(x, y, label=date)
       
    ax.legend() 
    ax.set_title('Topic Modelling, frequency against topics')
    ax.set_xlabel('Topics')
    ax.set_ylabel('Frequency')
    ###
   
    #### PLOT frequency against date 
    
    # Transform data into better DataFrame format
    from collections import defaultdict
    frames = []
   
    ax2 = fig.add_subplot(122)
    
    # build a new Dataframe
    for date in aggregated_data.index.levels[0]:
        frames.append(aggregated_data.loc[date])
        
    aggregated_data2 = pd.concat(frames, axis=1)
    aggregated_data2.columns = aggregated_data.index.levels[0]
    aggregated_data2 = aggregated_data2.fillna(0)
    
    for topic in aggregated_data2.index:
        x = aggregated_data2.columns
        y = aggregated_data2.loc[topic]
        ax2.plot(x, y, label=topic)
    
    # reset figure
    filename = "topicmodelling2.png"
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    ax2.legend()
    ax2.set_title('Topic Modelling, frequency against date')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Frequency')
    fig.savefig(path)
    
    html_text = mpld3.fig_to_html(fig) 
    
    return html_text 
    
def train_lda(doc_term_matrix, dictionary):
    """Apply the LDA Model """
    start = time.time()
    print('Training model this will take a while')
    
    ### Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    # Running and Training LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)
    
    #--------------------- Get all the topics ------------------------
    topics = ldamodel.print_topics(num_topics=10, num_words=2);
    print(topics)
    
    #------------------ Save / Load LDA model --------------------
    
    filename = 'lda_model'
    
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename) 
    ldamodel.save(path)
    print("LDA model saved and trained, it took {}".format(time.time()-start))
    
if __name__ == '__main__':
    # train LDA model
    # topic_modelling('train')
    
    # test LDA model
    topic_modelling('test')