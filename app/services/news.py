import os
from newsapi import NewsApiClient
from typing import List, Dict, Optional
from dotenv import load_dotenv
from functools import lru_cache
from datetime import datetime, timedelta
import logging
from fastapi import Request
from ..core.limiter import limiter

logger = logging.getLogger(__name__)
load_dotenv()

news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

@lru_cache(maxsize=100)
@limiter.limit("5/minute")
async def get_stock_news(request: Request, company_name: str, ticker: str) -> List[Dict]:
    """
    Fetch news articles for a given company and stock ticker.
    Uses caching to improve performance and rate limiting to prevent API abuse.
    """
    try:
        logger.info(f"Fetching news for {company_name} ({ticker})")
        news = news_api.get_everything(
            q=f"{company_name} OR {ticker}",
            language='en',
            sort_by='relevancy',
            page_size=5,
            from_param=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        )
        
        if not news or 'articles' not in news:
            logger.warning(f"No news found for {company_name} ({ticker})")
            return []
            
        articles = [
            {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "published_at": article["publishedAt"],
                "source": article["source"]["name"]
            }
            for article in news["articles"]
            if all(key in article for key in ["title", "description", "url", "publishedAt", "source"])
        ]
        
        logger.info(f"Found {len(articles)} news articles for {ticker}")
        return articles
    except Exception as e:
        logger.error(f"Error fetching news for {company_name} ({ticker}): {e}", exc_info=True)
        return []
