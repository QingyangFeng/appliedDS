from __future__ import print_function 
import twitter
import json

#original
api = twitter.Api(consumer_key='qVOsttE8wU9QkFT4Hfo3FJShG',
                  consumer_secret='PyQeas2I3ReJjce6bvWZ2z0Z2ceSRaFddvpJhIWzkbutfQaraV',
                  access_token_key='2906201207-Jkdm0qvch1WZqpm17fYrKaLBuh2W2L8973STTIk',
                  access_token_secret='cLxEVW8HPKDCRMYVMZBZuu9ww0y3mtgfYoZexQoHxvzmo')

# # I have reached limit by accident so created a new one
# api = twitter.Api(consumer_key='tNqeW4s0VMreGFrgRfqIJ5KKg',
#                   consumer_secret='NdrBEbwJUxBPba0VtU6wKU2zEJLCFNzN99R1ziLwZWUpVs1PP6',
#                   access_token_key='935870743757418496-Wu5NaRQZ5Bz7CO8wz4lTmtWIVfNcBfn',
#                   access_token_secret='qBRAExVFaSdBXUwS6dI1XZsAU1gFCxXU7iluhzvBJSo75')

assert isinstance(api.VerifyCredentials(), twitter.models.User)


def get_user(screen_name, count=2):
    # statuses are the the posts of a users timeline
    statuses = api.GetUserTimeline(screen_name=screen_name, count=count)
    
    assert isinstance(statuses, list)
    
    return statuses
    # data['text'] = statuses.text
    # data['created_at'] = statuses.create_at
    # data['name'] = statuses.name
    # data['time_zone'] = statuses.time_zone
    # data['profile_image_url_https'] = statuses.profile_image_url_https
    
def get_friends(screen_name, total_count=2):
    friends = api.GetFriends(screen_name=screen_name, total_count=total_count)

    return friends

"""
{"created_at": "Tue Mar 13 15:27:18 +0000 2018",
"favorite_count": 26105, "hashtags": [], 
"id": 973581274215473153, "id_str": "973581274215473153", 
"lang": "en", "retweet_count": 7499, 
"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", 
"text": "California\u2019s sanctuary policies are illegal and unconstitutional and put the safety and security of our entire nati\u2026 https://t.co/zaPkbqbRDM", 
"truncated": true, "urls": [{"expanded_url": "https://twitter.com/i/web/status/973581274215473153", "url": "https://t.co/zaPkbqbRDM"}], 
"user": {"created_at": "Wed Mar 18 13:46:38 +0000 2009", 
"description": "45th President of the United States of America\ud83c\uddfa\ud83c\uddf8", 
"favourites_count": 24, "followers_count": 48969884, 
"friends_count": 45, "geo_enabled": true, "id": 25073877, "id_str": "25073877", 
"lang": "en", "listed_count": 85746, "location": "Washington, DC", 
"name": "Donald J. Trump", "profile_background_color": "6D5C18", 
"profile_background_image_url": "http://pbs.twimg.com/profile_background_images/530021613/trump_scotland__43_of_70_cc.jpg", 
"profile_background_image_url_https": "https://pbs.twimg.com/profile_background_images/530021613/trump_scotland__43_of_70_cc.jpg", 
"profile_background_tile": true, "profile_banner_url": "https://pbs.twimg.com/profile_banners/25073877/1520890098", 
"profile_image_url": "http://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg", 
"profile_image_url_https": "https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg",
"profile_link_color": "1B95E0", "profile_sidebar_border_color": "BDDCAD", "profile_sidebar_fill_color": "C5CEC0",
"profile_text_color": "333333", "profile_use_background_image": true, "screen_name": "realDonaldTrump", 
"statuses_count": 37119, "time_zone": "Eastern Time (US & Canada)", "url": "https://t.co/OMxB0x7xC5",
"utc_offset": -14400, "verified": true}, "user_mentions": []}

Extracting n text from timeline
text posted
twitter profile image
"""
