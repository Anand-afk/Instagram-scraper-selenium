#!/usr/bin/env python3

from instaloader import Instaloader, Profile
import datetime

MAX_DAYS = 50

LIKES_WEIGHT = 1
COMMENTS_WEIGHT = 1
NUM_FOLLOWERS_WEIGHT = 1
NUM_POSTS_WEIGHT = 1

def get_summary(profile):
    user = {}

    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    current_date = datetime.datetime.now()
 
    for post in profile.get_posts():
        delta = current_date - post.date
        if (delta.days > MAX_DAYS):
            break
        if (post.likes is not None):
            total_num_likes += post.likes
        if (post.comments is not None):
            total_num_comments += post.comments
       
        total_num_posts += 1
    
        engagement = 0
        if profile.followers > 10000 and total_num_posts > 50:
            user['Username']=profile.username
            engagement = float( (LIKES_WEIGHT * total_num_likes) + (COMMENTS_WEIGHT * total_num_comments)) / ((NUM_FOLLOWERS_WEIGHT * profile.followers) * (NUM_POSTS_WEIGHT * total_num_posts))
            user['engagement'] = engagement * 100
            user['num_recent_posts'] = total_num_posts
            post_freq = 0.0
            if (total_num_posts > 0):
                post_freq = float(MAX_DAYS) / total_num_posts
            user['post_frequency'] = post_freq

            return user
            
import threading
from instaloader import Instaloader, Profile
import pickle

loader = Instaloader()
NUM_POSTS = 10
loader.login('your username','your password')

def get_hashtags_posts(query):
    posts = loader.get_hashtag_posts(query)
    users = {}
    count = 0
    for post in posts:
        profile = post.owner_profile
#         print(profile.username)
        summary = get_summary(profile)
        if summary != None:
            users[profile.username] = summary
            count += 1
            print('{}: {}'.format(count, users[profile.username]))
        if count == NUM_POSTS:
            break
    return users

if __name__ == "__main__":
    hashtag = "beardcare"
    users = get_hashtags_posts(hashtag)
    print(users)