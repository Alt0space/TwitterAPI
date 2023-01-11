import configparser
import json
from requests_oauthlib import OAuth1Session

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_secret_key']
api_access_token = config['twitter']['api_access_token']
api_access_token_secret = config['twitter']['api_access_token_secret']

# Create Auth Session
session = OAuth1Session(api_key, api_key_secret, api_access_token, api_access_token_secret)


# Get info about the user
def parse_user(username):
    response = session.get(f"https://api.twitter.com/1.1/users/show.json?screen_name={username}")
    if response.status_code < 200:
        status = 'pending'
    elif response.status_code > 399:
        status = 'failed'
    else:
        status = 'success'
    return json.loads(response.text), status


# Get User's tweets
def get_tweets(user_id):
    response = session.get(f"https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={user_id}&count=10")
    data = json.loads(response.text)
    return data

