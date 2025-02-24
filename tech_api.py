from newsapi import NewsApiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()
# Store these securely (e.g., in environment variables)
NEWS_API = os.getenv('NEWS_API')
# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=NEWS_API)
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def get_tech_news():
    """
    Fetch one piece of the latest technology or gaming news and format the output.
    Tries English first, falls back to Spanish if no English articles are found.
    """
    # Try English first
    news = newsapi.get_everything(
        q='technology OR gaming OR tech OR game OR playstation OR xbox OR nintendo OR apple OR cellphone OR phone OR PC',
        language='en',
        sort_by='popularity',
        from_param=yesterday,
        page_size=1
    )
    
    # If no English articles found, try Spanish
    if not news['articles']:
        news = newsapi.get_everything(
            q='tecnología OR videojuegos OR juego OR xbox OR playstation OR xbox OR nintendo OR apple OR celular OR telefono OR PC',
            language='es',
            sort_by='popularity',
            from_param=yesterday,
            page_size=1
        )
    
    if news['articles']:
        article = news['articles'][0]
        # Format the news information
        formatted_news = {
            "title": article.get("title", "No title available"),
            "author": article.get("author", "Unknown"),
            "source": article.get("source", {}).get("name", "Unknown source"),
            "description": article.get("description", "No description available"),
            "url": article.get("url", "No URL available"),
            "image_url": article.get("urlToImage", "No image available"),
            "published_at": article.get("publishedAt", "Unknown date"),
            "language": "en" if article.get("language", "en") == "en" else "es"
        }
        return formatted_news
    else:
        return "No articles found in English or Spanish!"

if __name__ == "__main__":
    tech_news = get_tech_news()
    if isinstance(tech_news, str):
        print(tech_news)  # Handle case where no articles are found
    else:
        if tech_news["language"] == "en":
            print("Latest Tech/Gaming News:")
            print(f"📰 Title: {tech_news['title']}")
            print(f"✍️ Author: {tech_news['author']}")
            print(f"📡 Source: {tech_news['source']}")
            print(f"📅 Published At: {tech_news['published_at']}")
            print(f"📝 Description: {tech_news['description']}")
            print(f"🔗 URL: {tech_news['url']}")
            print(f"🖼️ Image URL: {tech_news['image_url']}")
        else:
            print("Últimas noticias de tecnología/videojuegos:")
            print(f"📰 Título: {tech_news['title']}")
            print(f"✍️ Autor: {tech_news['author']}")
            print(f"📡 Fuente: {tech_news['source']}")
            print(f"📅 Publicado: {tech_news['published_at']}")
            print(f"📝 Descripción: {tech_news['description']}")
            print(f"🔗 URL: {tech_news['url']}")
            print(f"🖼️ URL de imagen: {tech_news['image_url']}")
