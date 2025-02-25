from typing import List, Dict
from datetime import datetime, timedelta
import logging
from fastapi import Request
from functools import lru_cache

logger = logging.getLogger(__name__)

@lru_cache(maxsize=100)
async def get_stock_news(request: Request, company_name: str, ticker: str) -> List[Dict]:
    """
    Fetch news articles for a given company and stock ticker.
    Uses caching to improve performance.
    """
    try:
        logger.info(f"Fetching news for {company_name} ({ticker})")
        
        # Mock news data for testing
        mock_news = [
            {
                "title": f"{company_name} Market Update",
                "description": f"Latest market analysis for {ticker}...",
                "url": "https://example.com/news/1",
                "published_at": datetime.now().isoformat(),
                "source": "Market News"
            },
            {
                "title": f"{company_name} Industry Trends",
                "description": f"Industry analysis for {ticker}...",
                "url": "https://example.com/news/2",
                "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "source": "Industry Insights"
            }
        ]
        
        logger.info(f"Returning mock news for {ticker}")
        return mock_news
            
    except Exception as e:
        logger.error(f"Error fetching news for {company_name} ({ticker}): {e}", exc_info=True)
        return []
