import json
import datetime
import nltk
import tweepy
import re
#from preprocessing import 
from sklearn.feature_extraction.text import CountVectorizer
from pymongo import MongoClient
#assume that the tweets are save in the cloud
client = MongoClient()
db = client.TwitterStream
collection = db.topic_v2
raw_timeline = db.timeline_v2
only_text = db.text
celebrity = db.celebrity
#Twitter API credentials
access_token = "3854934923-V2mzUpyTHgpbzEUwaVh2sEIn0QpsLwGIOhUDZBu"
access_token_secret = "qzaGkfmDG2VJweZ1zekdUUhDleIjFdpfY9aF89QNCEzcH"
consumer_key = "YKFwh5ZKl3ZdzLQ26bGJ4yJqi"
consumer_secret = "1I0rigWuuwfdwKL4uVTgC2sAyWa36Fhv0FCeJIIEd5TFd1Uqgm"
def getUserName():
  namelist=[]
  i = 0
  for tweet in db.tweet.find():
      if i < 1000:
         userName = tweet['username']
         namelist.append(userName)
      else:
         break
      i = i + 1  
  return namelist
  #print namelist
def getUserTimelinetweet(namelist):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #authorize twitter, initialize tweep
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #initialize a list to hold all the tweepy Tweets	
    #alltext=[]	
    for name in namelist:
        try:
        #make initial request for most recent tweets (100 is the maximum allowed count)
            tltweets = api.user_timeline(screen_name = name, count=100, tweet_mode="extended")
            alltext = []
            for oldtweet in tltweets:
                text = oldtweet.full_text
                alltext.append(text)
                screen_name = oldtweet.user.screen_name
                dt = oldtweet.created_at
                created ='{:%a %b %d %H:%M:%S +0000 %Y}'.format(dt)
                outtweets = {'username':screen_name,'created':created,'text':text}
            #raw timeline tweet save in collection timeline
                print(outtweets)
                raw_timeline.save(outtweets)
            #data will be used for analysising  saved in seperate collection
                analysis_content = {'username':name, 'paragraph': alltext}
               #only_text.save(analysis_content)
               #print alltext
        except tweepy.error.TweepError:
                continue         
def textAnalysis():
    vectorizer = CountVectorizer()
    mention_pattern = re.compile('\@\S+\s|$')
    emoji_pattern = re.compile(
      u"(\ud83d[\ude00-\ude4f])|"  # emoticons
      u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
      u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
      u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
      u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
      "+", flags=re.UNICODE)#emoji_pattern = re.compile('\S')
    corpus = []
    for data in db.text.find():
        paragraph = []
        for text in data['paragraph']:#.encode("utf-8") 
            text = text.lower() #change all the character into lowercase
            text = re.sub(r'http\S+','',text)#remove url
            text = re.sub(r'\n','',text)
            text = mention_pattern.sub(r'',text)#remove @username
            text = emoji_pattern.sub(r'',text)#remove emoji
            paragraph.append(text.encode('utf-8'))
            content = '.'.join(paragraph)
        corpus.append(content)
    x = vectorizer.fit_transform(corpus)
    print x.toarray()    
name = getUserName()       
#name = ['realDonaldTrump','BarackObama','BristolUni','Arsenal','TheRealStanLee','Selfridges','GordonRamsay']
getUserTimelinetweet(name)
#textAnalysis()
