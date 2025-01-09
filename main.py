import tweepy
import os
from Get_Games import *
from tech_api import get_tech_news
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET_KEY']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

# Initialize OAuth 1.0a handler
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET_KEY,
    callback='oob'  # Use 'oob' for testing/CLI apps
)

# Get the authorization URL
try:   
    # Create client with the authenticated tokens
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    tech_news = get_tech_news()
    # Try posting a tweet
    if isinstance(tech_news, dict):  # Ensure it is a dictionary
        # Format the tweet text
        Text = (
            f"📰 {tech_news['title']}\n" 
            f"📡 Source: {tech_news['source'] or 'Unknown source'}\n"
            f"🔗 {tech_news['url']}\n"
            "#TechNews #Gaming"
        )
    else:
        Text = "No tech news available at the moment!"

    response = client.create_tweet(text=Text)
    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")

except Exception as e:
    print(f"Error: {e}")
