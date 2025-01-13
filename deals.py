import requests
import time
from datetime import datetime
from typing import List, Optional, Dict

class GameDealsFinder:
    def __init__(self):
        self.base_url = "https://www.cheapshark.com/api/1.0"
        self.stores = self.get_stores()
        
    def get_stores(self) -> Dict[str, dict]:
        """Fetch and return all available stores from CheapShark API"""
        response = requests.get(f"{self.base_url}/stores")
        if response.status_code == 200:
            stores_dict = {}
            for store in response.json():
                stores_dict[str(store['storeID'])] = {
                    'name': store['storeName'],
                    'is_active': store['isActive'],
                    'images': {
                        'banner': f"https://www.cheapshark.com{store['images']['banner']}",
                        'logo': f"https://www.cheapshark.com{store['images']['logo']}",
                        'icon': f"https://www.cheapshark.com{store['images']['icon']}"
                    }
                }
            return stores_dict
        return {}

    def generate_hashtags(self, deal: dict, store_name: str) -> str:
        """Generate relevant hashtags for the deal"""
        hashtags = ["#GameDeals"]
        
        # Add store-specific hashtag
        store_hashtag = f"#{store_name.replace(' ', '')}"
        hashtags.append(store_hashtag)
        
        # Add gaming hashtags
        hashtags.append("#Gaming")
        
        # Add price-based hashtags
        if float(deal['savings']) >= 75:
            hashtags.append("#BigSale")
        
        # Add rating-based hashtags
        if deal.get('metacriticScore') and float(deal['metacriticScore']) >= 85:
            hashtags.append("#MustPlay")
        
        # Game title hashtag (simplified)
        game_hashtag = "#" + "".join(x for x in deal['title'] if x.isalnum())
        if len(game_hashtag) > 2:  # Only add if meaningful
            hashtags.append(game_hashtag)
            
        return " ".join(hashtags)

    def format_tweet(self, deal: dict) -> str:
        """
        Format a single deal as a tweet (max 280 characters)
        Returns a tweet-ready string
        """
        store_name = self.stores.get(deal['storeID'], {}).get('name', 'Unknown Store')
        savings = round(float(deal['savings']), 1)
        
        # Format price strings
        sale_price = f"${deal['salePrice']}"
        normal_price = f"${deal['normalPrice']}"
        
        # Start with alert and the game title
        tweet = f"🚨 New Deal Alert: 🎮\n\n"
        tweet += f"{deal['title']}\n"
        tweet += f"💰 {sale_price} (was {normal_price}, -{savings}%)\n"
        tweet += f"🏪 {store_name}\n"
        
        # Add ratings if available
        ratings = []
        if deal.get('metacriticScore'):
            ratings.append(f"MC: {deal['metacriticScore']}")
        if deal.get('steamRatingPercent'):
            ratings.append(f"Steam: {deal['steamRatingPercent']}%")
        
        if ratings:
            tweet += f"⭐ {' | '.join(ratings)}\n"
        
        # Add deal URL
        tweet += f"🔗 https://www.cheapshark.com/redirect?dealID={deal['dealID']}\n"
        
        # Generate and add hashtags if there's room
        hashtags = self.generate_hashtags(deal, store_name)
        if len(tweet) + len(hashtags) <= 280:
            tweet += f"\n{hashtags}"
            
        return tweet

    def format_all_tweets(self, deals: list) -> List[str]:
        """Format all deals as tweets"""
        return [self.format_tweet(deal) for deal in deals]

    def get_game_deals(
        self,
        store_ids: Optional[List[str]] = None,
        page_number: int = 0,
        page_size: int = 60,
        sort_by: str = "DealRating",
        desc: bool = True,
        min_price: float = 0,
        max_price: Optional[float] = None,
        min_metacritic: Optional[int] = None,
        min_steam_rating: Optional[int] = None,
        max_age_hours: Optional[int] = None,
        steam_app_ids: Optional[List[str]] = None,
        title: Optional[str] = None,
        exact_match: bool = False,
        aaa_only: bool = False,
        steamworks_only: bool = False,
        on_sale_only: bool = True,
        output_format: Optional[str] = None
    ):
        """[Previous implementation remains the same]"""
        # [Previous implementation remains the same]
        if store_ids:
            store_ids = [sid for sid in store_ids if self.stores.get(sid, {}).get('is_active', False)]
            
        params = {
            "pageNumber": page_number,
            "pageSize": min(page_size, 60),
            "sortBy": sort_by,
            "desc": 1 if desc else 0,
            "lowerPrice": min_price,
            "onSale": 1 if on_sale_only else 0,
            "AAA": 1 if aaa_only else 0,
            "steamworks": 1 if steamworks_only else 0,
        }
        
        if store_ids:
            params["storeID"] = ",".join(store_ids)
        if max_price:
            params["upperPrice"] = max_price
        if min_metacritic:
            params["metacritic"] = min_metacritic
        if min_steam_rating:
            params["steamRating"] = min_steam_rating
        if max_age_hours:
            params["maxAge"] = max(1, min(max_age_hours, 2500))
        if steam_app_ids:
            params["steamAppID"] = ",".join(steam_app_ids)
        if title:
            params["title"] = title
            params["exact"] = 1 if exact_match else 0
        if output_format:
            params["output"] = output_format

        response = requests.get(f"{self.base_url}/deals", params=params)
        
        if response.status_code != 200:
            print(f"Error fetching deals: {response.status_code}")
            return None
            
        deals = response.json()
        total_pages = int(response.headers.get('X-Total-Page-Count', 0))
        
        return deals, total_pages

    def print_tweets(self, deals_data):
        """Print deals in tweet format"""
        if not deals_data or not deals_data[0]:
            print("No deals found matching the criteria.")
            return
            
        deals, total_pages = deals_data
        print(f"\nFound {len(deals)} deals (Total pages: {total_pages})")
        print("=" * 80)
        
        tweets = self.format_all_tweets(deals)
        for i, tweet in enumerate(tweets, 1):
            print(f"\nTweet {i}:")
            print("-" * 40)
            print(tweet)
            print(f"Characters: {len(tweet)}/280")
            print("-" * 40)

if __name__ == "__main__":
    finder = GameDealsFinder()
    
    # Example usage with multiple stores
    search_params = {
        "store_ids": ["1", "7", "8", "11", "25"],  # Steam, GOG, Origin, Humble Store, Epic
        "min_price": 1,
        "max_price": 100,
        "min_metacritic": 35,
        "min_steam_rating": 45,
        "max_age_hours": 108,
        "sort_by": "Savings",
        "desc": True,
        "aaa_only": True,
        "steamworks_only": False,
        "on_sale_only": True,
        "page_size": 20  # Reduced to show fewer tweets as example
    }
    
    print("Searching for game deals...")
    deals_data = finder.get_game_deals(**search_params)
    finder.print_tweets(deals_data)
