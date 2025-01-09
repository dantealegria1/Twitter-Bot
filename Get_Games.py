import random
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
class RAWGGameFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api"

    def get_random_game(self):
        try:
            # Generate a random page and fetch game list
            random_page = random.randint(1, 1000)
            games_response = requests.get(f"{self.base_url}/games?key={self.api_key}&page={random_page}")
            games_response.raise_for_status()
            games_data = games_response.json()

            # Select a random game from the list
            game = random.choice(games_data.get('results', []))
            game_id = game['id']

            # Fetch detailed game information
            detailed_response = requests.get(f"{self.base_url}/games/{game_id}?key={self.api_key}")
            detailed_response.raise_for_status()
            detailed_game = detailed_response.json()

            # Extract genres and tags
            genres = [genre['name'] for genre in detailed_game.get('genres', [])]
            tags = [tag['name'] for tag in detailed_game.get('tags', [])]

            # Extract description
            description = detailed_game.get('description_raw', 'No description available')

            # Fetch store information
            stores_response = requests.get(f"{self.base_url}/games/{game_id}/stores?key={self.api_key}")
            stores_response.raise_for_status()
            stores_data = stores_response.json()

            # Find Steam store URL if it exists
            steam_url = None
            for store in stores_data.get('results', []):
                if store['store_id'] == 1:  # 1 is Steam's store ID in RAWG
                    steam_url = store['url']
                    break

            # Build game information
            game_info = {
                'name': game['name'],
                'release_date': game.get('released', 'Unknown'),
                'genres': genres,
                'tags': tags,
                'rating': game.get('rating', 'N/A'),
                'description': description,
                'image_url': game.get('background_image', None),
                'steam_url': steam_url
            }
            return game_info

        except requests.exceptions.RequestException as e:
            return f"Error fetching game data: {str(e)}"

    def format_game_tweet(self, game_info):
        """
        Format game information into a tweet-sized message.
        """
        if isinstance(game_info, str):  # If there was an error
            return game_info

        tweet = f"Daily Game you should try: \n"
        tweet += f"🎮 {game_info['name']}\n"
        tweet += f"📅 Release: {game_info['release_date']}\n"

        if game_info['genres']:
            tweet += f"🎯 Genres: {', '.join(game_info['genres'][:3])}\n"

        if game_info['rating']:
            tweet += f"⭐ Rating: {game_info['rating']}/5\n"

        if game_info['description']:
            tweet += f"📝 {game_info['description'][:100]}...\n"

        if game_info.get('steam_url'):
            tweet += f"🎯 Steam: {game_info['steam_url']}\n"

        tweet += "\n#gaming #videogames"
        return tweet

def send_info():
    API_KEY = os.getenv('GAMES_API_KEY')
    game_fetcher = RAWGGameFetcher(API_KEY)
    random_game_info = game_fetcher.get_random_game()
    content = game_fetcher.format_game_tweet(random_game_info)
    return content

# Example usage
if __name__ == "__main__":
    API_KEY = os.getenv('GAMES_API_KEY')
    game_fetcher = RAWGGameFetcher(API_KEY)

    # Get a random game
    random_game_info = game_fetcher.get_random_game()

    # Print full game info
    print("Random Game Information:")
    print(json.dumps(random_game_info, indent=2))

    # Print tweet format
    print("\nTweet Format:")
    content = game_fetcher.format_game_tweet(random_game_info)
    print(content)
