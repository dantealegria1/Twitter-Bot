import tweepy
import os
import re
from Get_Games import *
from tech_api import get_tech_news
from dotenv import load_dotenv

def generate_hashtags(text):
    """
    Generate hashtags from the text of the news article
    
    Args:
        text (str): Text to generate hashtags from
    
    Returns:
        str: Hashtags string
    """
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter and capitalize words to create hashtags
    hashtags = ['#' + word.capitalize() for word in set(words) 
                if len(word) > 3 and word not in ['with', 'from', 'this', 'that', 'tech']]
    
    # Limit to 3 hashtags
    hashtags = hashtags[:3]
    
    # Ensure we always have some hashtags
    if not hashtags:
        hashtags = ['#TechNews', '#Innovation']
    
    return ' '.join(hashtags)

# Load environment variables from .env file
load_dotenv()
API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
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
    
    # Format the tweet text
    if isinstance(tech_news, dict):  # Ensure it is a dictionary
        # Generate hashtags from the title
        dynamic_hashtags = generate_hashtags(tech_news['title'])
        
        Text = (
            f"📰 {tech_news['title']}\n" 
            f"📡 Source: {tech_news['source'] or 'Unknown source'}\n"
            f"🔗 {tech_news['url']}\n"
            f"{dynamic_hashtags}"
        )
    else:
        Text = "No tech news available at the moment!"
    
    response = client.create_tweet(text=Text)
    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
except Exception as e:
    print(f"Error: {e}")
