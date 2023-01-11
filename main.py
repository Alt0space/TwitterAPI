from fastapi import FastAPI, HTTPException, Request
from logic import parse_user, get_tweets
import re

app = FastAPI()

# Data storage
parsing_session = {"last_id": 0}
parsed_users = {}
parsed_tweets = {}


# Main method to parse list of Users
# Post body should look like this:
# {"account_links": ["link1","link2"]}

@app.post("/api/parse/")
async def parse_accounts(request: Request):
    data = await request.json()
    account_links = data["account_links"]
    session_id = parsing_session['last_id'] + 1
    parsing_session['last_id'] = session_id
    users_in_ses = []
    for user in account_links:
        username = re.search(r"twitter\.com/(\w+)", user).group(1)
        data, status = parse_user(username)
        user_status = {
            'username': username,
            'status': status
        }
        parsed_user_info = {"twitter_id": data['id'], "name": data["name"], "username": data['screen_name'], "following_count": data["friends_count"], "followers_count": data["followers_count"], "description": data["description"]}
        users_in_ses.append(user_status)
        parsed_users[username] = parsed_user_info
        tweets_raw = get_tweets(data['id'])
        tweets = []
        for tweet in tweets_raw:
            tweets.append(tweet['text'])
        parsed_tweets[data['id']] = tweets
    parsing_session[session_id] = users_in_ses
    return {"session_id": session_id}


@app.get("/api/status/{session_id}")
async def get_status(session_id: int):
    if session_id not in parsing_session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return parsing_session[session_id]


@app.get("/api/user/{username}")
async def get_user_info(username: str):
    if username not in parsed_users:
        raise HTTPException(status_code=404, detail="User not found in previous sessions.")
    return parsed_users[username]


@app.get("/api/tweets/{twitter_id}")
async def get_user_tweets(twitter_id: int):
    if twitter_id not in parsed_tweets:
        raise HTTPException(status_code=404, detail="This twitter_id not found in previous sessions.")
    return parsed_tweets[twitter_id]
