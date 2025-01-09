
from newsapi import NewsApiClient

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key='a269ba68b9a54a6f9259f24acff47662')

def get_tech_news():
    """
    Fetch one piece of the latest technology or gaming news and format the output.
    """
    news = newsapi.get_everything(
        q='technology OR gaming',
        language='en',
        sort_by='publishedAt',
        page_size=1  # Fetch only one article
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
            #"content": article.get("content", "No content available"),
        }

        return formatted_news
    else:
        return "No articles found!"

# Example usage
if __name__ == "__main__":
    tech_news = get_tech_news()

    if isinstance(tech_news, str):
        print(tech_news)  # Handle case where no articles are found
    else:
        print("Latest Tech/Gaming News:")
        print(f"📰 Title: {tech_news['title']}")
        print(f"✍️ Author: {tech_news['author']}")
        print(f"📡 Source: {tech_news['source']}")
        print(f"📅 Published At: {tech_news['published_at']}")
        print(f"📝 Description: {tech_news['description']}")
        print(f"🔗 URL: {tech_news['url']}")
        print(f"🖼️ Image URL: {tech_news['image_url']}")
        print(f"📖 Content: {tech_news['content']}")
