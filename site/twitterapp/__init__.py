from __future__ import print_function 
from flask import Flask, render_template, request, redirect, Response
from nocache import nocache

from os.path import join, dirname, realpath
import sys

# Serving dynamic images with Pandas and matplotlib (using flask)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['DEBUG'] = True


@app.route("/")
@nocache
def index():
    return render_template('index.html')
        

"""Get Twitter Stream data"""
    
@app.route("/user")
@nocache
def user():
    return render_template('index_.html')
    
# @app.route("/user/results")
# @nocache
# def userinfo(username):
#     """user tweets
#     collect the first n tweets
#     able to pass in an arbitrary amount of messages into HTML.
#     """
#     return render_template('live.html')

@app.route("/streamdata/<username>/<int:count>/json")
# @app.route("/streamdata/json")
@nocache
def streamdata(username, count):
    from  Modules.usertweets import get_user
    
    messages = get_user(username, count)
    # return json.dumps([s.text for s in messages])
    return json.dumps([s.AsJsonString() for s in messages])
    
@app.route("/test")
@nocache
def test():
    return render_template('live.html')



@app.route("/friends/<username>", methods=["POST"])
@nocache
def friends(username):
    from  Modules.usertweets import get_friends
    
    friends = get_friends(username)
    screenNames = [friend.screen_name for friend in friends]

    return json.dumps(screenNames)


@app.route("/common_friends/<username>")
@nocache
def commonFriends(username):
    "I am currently using only 2 friends limit, so that I don't reach limit instantly"
    from  Modules.usertweets import get_friends
    
    friends = get_friends(username)
    screenNames = [friend.screen_name for friend in friends]
    common = {}
    for screenName in screenNames:
        friendsOfFriend = get_friends(screenName)
        common[screenName] = [screenName if friend.screen_name in screenNames else '' for friend in friendsOfFriend]


    return json.dumps(common)

@app.route("/similar/<username>")
@nocache
def similar(username):
    from Modules.usertweets import get_user
    from Modules.recommends import get_most_similar_bag_of_words_based

    messages = get_user(username, 25)
    oneString = ''.join([s.text for s in messages])

    return json.dumps(get_most_similar_bag_of_words_based(oneString))


@app.route("/getMessages", methods=["POST"])
@nocache
def getMessages():
    from Modules.usertweets import get_user
    
    data = request.get_json(force=True)
    username = data.get('username')

    messages = get_user(username, 25) # Big values might be a bit wasteful on API calls, but who knows!
    arrayOfTweets =  [tweet.text for tweet in messages]
    
    return json.dumps(arrayOfTweets)

@app.route("/getUserSentiment", methods=["POST"])
@nocache
def getUserSentiment():
    from Modules.usertweets import get_user
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    #  force=True returns an object 
    data = request.get_json(force=True)
    username = data.get('username')

    messages = get_user(username, 10) # Big values might be a bit wasteful on API calls, but who knows!
    arrayOfTweets =  [tweet.text for tweet in messages]
    stringOfTweets = ''.join(arrayOfTweets)

    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(stringOfTweets)
    return json.dumps(scores)

@app.route("/getTopicModelling")
@nocache
def getTopicModelling():
    from Modules.TopicModellingScript import topic_modelling
    html_text = topic_modelling('test')
    return html_text
    

if __name__ == "__main__":
    app.run(debug=True)
    # debug = True will turn off jinja2 caching