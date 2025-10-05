from google_news_api import GoogleNewsClient

class NewsAPI:
    def fetch_news(self, ticker: str):
        client = GoogleNewsClient(
            language="en",
            country="US",
            requests_per_minute=60,
            cache_ttl=300
        )

        articles = client.search(f"{ticker} stocks", when="7d", max_results = 3)

        for article in articles:
            return [f"{article['title']}"]
        #for topic in news.items:

        #    return article.title
        #return [f"{ticker} hits record high!", f"{ticker} faces market challenges"]
