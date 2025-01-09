import tweepy
import os

# Get credentials from environment variables
api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET_KEY']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

# Initialize tweepy client
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Test authentication
try:
    # Try to get your own user info
    me = client.get_me()
    print("Authentication successful!")
    print(f"Connected as: {me.data.username}")
except tweepy.TweepyException as e:
    print(f"Authentication failed: {str(e)}")
