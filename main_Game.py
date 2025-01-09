import tweepy
import os
from Get_Games import send_info
from dotenv import load_dotenv

load_dotenv()
# Store these securely (e.g., in environment variables)
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY') 
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

# Initialize OAuth 1.0a handler
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET_KEY,
    callback='oob'  # Use 'oob' for testing/CLI apps
)

try:
    # Create client
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    # Get game info and post tweet
    game = send_info()
    response = client.create_tweet(text=game)
    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")

except tweepy.TweepyException as e:
    print(f"Twitter API error: {str(e)}")
except Exception as e:
    print(f"General error: {str(e)}")
