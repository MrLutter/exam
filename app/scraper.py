import requests
import feedparser
import json
from time import mktime
from datetime import datetime
import os # Required for os.path.join and os.path.dirname

SOURCES = [
    {
        "name": "Google AI Blog",
        "rss_url": "https://ai.googleblog.com/atom.xml"
    },
    {
        "name": "OpenAI Blog",
        "rss_url": "https://openai.com/blog/rss/"
    },
    {
        "name": "TechCrunch AI",
        "rss_url": "https://techcrunch.com/category/artificial-intelligence/feed/"
    }
]

def fetch_news():
    all_articles = []
    for source in SOURCES:
        print(f"Fetching news from: {source['name']}")
        try:
            feed = feedparser.parse(source['rss_url'])
            for entry in feed.entries:
                title = entry.get("title")
                link = entry.get("link")
                
                # Try to get parsed publication date
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    # Format yyyy-mm-dd
                    try:
                        dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                        pub_date = dt.strftime('%Y-%m-%d')
                    except TypeError: # Handle cases where published_parsed is not a valid time tuple
                        pub_date = entry.get("published", "N/A")

                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed: # some feeds use 'updated' instead of 'published'
                    try:
                        dt = datetime.fromtimestamp(mktime(entry.updated_parsed))
                        pub_date = dt.strftime('%Y-%m-%d')
                    except TypeError:
                        pub_date = entry.get("updated", "N/A")
                else: # Fallback to raw published string
                    pub_date = entry.get("published", entry.get("updated", "N/A"))

                article = {
                    "title": title,
                    "link": link,
                    "publication_date": pub_date,
                    "source": source['name']
                }
                all_articles.append(article)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching feed from {source['rss_url']}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {source['name']}: {e}")

    # Sort articles by publication date (descending)
    # Handle cases where pub_date might be "N/A" or not a valid date string for sorting
    all_articles.sort(key=lambda x: x['publication_date'] if x['publication_date'] and x['publication_date'] != "N/A" else '0000-00-00', reverse=True)
    
    return all_articles

def save_news_to_json(news_data, filename="news_data.json"):
    # Corrected filepath to be relative to the scraper.py's location
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(filepath, 'w') as f:
            json.dump(news_data, f, indent=4)
        print(f"Successfully saved news data to {filepath}")
    except IOError as e:
        print(f"Error saving news data to {filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving to JSON: {e}")


if __name__ == "__main__":
    print("Starting news fetching process...")
    articles = fetch_news()
    if articles:
        save_news_to_json(articles)
        print(f"Successfully fetched and saved {len(articles)} articles to app/news_data.json")
    else:
        print("No articles fetched. Nothing to save.")
