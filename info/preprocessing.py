from pymongo import MongoClient
import json
import re
import datetime
client = MongoClient('129.150.114.173')
db = client.TwitterStream
collection = db.tweet
collection2 = db.preprocessing
data = [] 
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

for tweet in db.tweet.find():
	
        tweet['text'] = tweet['text'].lower() #change all the character into lowercase
	tweet['text'] = re.sub(r'http\S+','',tweet['text'])#remove url
	tweet['text'] = mention_pattern.sub(r'',tweet['text'])#remove @username
	#tweet['text'] = re.sub(r'&amp','',tweet['text'])#remove retweet
	#tweet['text'] = hashtag_pattern.sub(r'',tweet['text'])#remove hashtag
	tweet['text'] = emoji_pattern.sub(r'',tweet['text'])#remove emoji
	if not any(bad_word in tweet['text'] for bad_word in bad_words):	
		print tweet['text']#remove obivous noice	
        #if you want to save back into mongodb, define another collection first  
        collection2.save(tweet)
		 
