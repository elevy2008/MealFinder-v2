import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def get_stock_data(request: Request, ticker: str) -> Optional[Dict]:
    """Get current stock data with mock data for testing."""
    try:
        logger.info(f"Fetching stock data for {ticker}")
        
        # Mock data for testing
        if ticker == "AAPL":
            mock_data = {
                "current_price": 150.25,
                "previous_close": 149.50,
                "day_high": 151.00,
                "day_low": 148.75,
                "volume": 1000000,
                "market_cap": 2500000000,
                "company_name": "Apple Inc."
            }
        else:
            mock_data = {
                "current_price": 100.00,
                "previous_close": 99.50,
                "day_high": 101.00,
                "day_low": 98.75,
                "volume": 500000,
                "market_cap": 1000000000,
                "company_name": f"Company {ticker}"
            }
            
        logger.info(f"Returning mock data for {ticker}")
        return mock_data
            
    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}", exc_info=True)
        return None

async def get_stock_history(ticker: str, period: str = "1mo") -> Optional[List[Dict]]:
    """Get stock price history with mock data for testing."""
    try:
        logger.info(f"Fetching historical data for {ticker}")
        
        # Generate mock historical data
        mock_history = []
        base_price = 150.0 if ticker == "AAPL" else 100.0
        
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            mock_history.append({
                "date": date.strftime("%Y-%m-%d"),
                "close": base_price + (i % 5),
                "volume": 1000000 - (i * 10000)
            })
            
        logger.info(f"Returning mock historical data for {ticker}")
        return mock_history
        
    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}", exc_info=True)
        return None
