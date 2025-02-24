from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from ..schemas.user import PortfolioAdd
from ..services.auth import get_current_user
from ..services.stock import get_stock_data, get_stock_history
from ..services.news import get_stock_news
from typing import Dict, List, Optional
import uuid
import logging
import json
import asyncio
from datetime import datetime
from ..core.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

# In-memory portfolio storage
portfolios: Dict[str, List[dict]] = {}

@router.post("/holdings")
async def add_holding(
    request: Request,
    holding: PortfolioAdd,
    user_id: str = Depends(get_current_user)
):
    try:
        logger.info(f"Adding holding for user {user_id}: {holding.ticker}")
        
        # Get stock data
        stock_data = await get_stock_data(request, holding.ticker)
        if not stock_data:
            logger.error(f"Invalid stock ticker: {holding.ticker}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Invalid stock ticker: {holding.ticker}"}
            )
        
        # Initialize user portfolio if needed
        if user_id not in portfolios:
            portfolios[user_id] = []
            logger.info(f"Created new portfolio for user {user_id}")
        
        # Create new holding
        new_holding = {
            "id": str(uuid.uuid4()),
            "ticker": holding.ticker.upper(),
            "amount": holding.amount,
            "current_data": stock_data
        }
        portfolios[user_id].append(new_holding)
        logger.info(f"Successfully added holding: {new_holding}")
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Holding added successfully", "data": new_holding}
        )
    except Exception as e:
        logger.error(f"Error adding holding: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )

@router.get("/holdings")
async def get_holdings(
    request: Request,
    user_id: str = Depends(get_current_user)
) -> List[Dict]:
    start_time = datetime.now()
    logger.info(
        "Getting holdings",
        extra={
            "user_id": user_id,
            "path": request.url.path,
            "method": request.method,
            "process_time": (datetime.now() - start_time).total_seconds()
        }
    )
    return portfolios.get(user_id, [])

@router.delete("/holdings/{holding_id}")
async def remove_holding(
    request: Request,
    holding_id: str,
    user_id: str = Depends(get_current_user)
):
    start_time = datetime.now()
    logger.info(
        "Removing holding",
        extra={
            "user_id": user_id,
            "holding_id": holding_id,
            "path": request.url.path,
            "method": request.method,
            "process_time": (datetime.now() - start_time).total_seconds()
        }
    )
    
    if user_id not in portfolios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found"
        )
    
    portfolios[user_id] = [
        h for h in portfolios[user_id]
        if h["id"] != holding_id
    ]
    
    return {"message": "Holding removed successfully"}

@router.get("/analysis")
@limiter.limit("5/minute")
async def get_portfolio_analysis(
    request: Request,
    user_id: str = Depends(get_current_user)
):
    try:
        logger.info(f"Getting portfolio analysis for user {user_id}")
        holdings = portfolios.get(user_id, [])
        
        if not holdings:
            logger.info(f"No holdings found for user {user_id}")
            return []
            
        analysis = []
        for holding in holdings:
            try:
                # Use existing stock data from holdings
                stock_data = holding.get("current_data")
                if not stock_data:
                    logger.error(f"No stock data found for {holding['ticker']}")
                    continue
                
                # Get historical data
                history = await get_stock_history(holding["ticker"])
                if not history:
                    logger.warning(f"No history data found for {holding['ticker']}")
                    history = []
                
                # Get news data
                news = await get_stock_news(request, stock_data["company_name"], holding["ticker"])
                if not news:
                    logger.warning(f"No news found for {holding['ticker']}")
                    news = []
                
                analysis.append({
                    "ticker": holding["ticker"],
                    "amount": holding["amount"],
                    "current_data": stock_data,
                    "history": history,
                    "news": news
                })
                logger.info(f"Successfully analyzed {holding['ticker']}")
            except Exception as e:
                logger.error(f"Error analyzing {holding['ticker']}: {e}", exc_info=True)
                continue
        
        return analysis
    except Exception as e:
        logger.error(f"Error getting portfolio analysis: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
