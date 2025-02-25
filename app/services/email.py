from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime
from .stock import get_stock_data
from .news import get_stock_news

load_dotenv()

# Initialize email config only if credentials are present
conf = None
if all([os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"), os.getenv("MAIL_FROM")]):
    conf = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)

async def send_daily_summary(email: str, holdings: List[Dict]):
    content = "Daily Portfolio Summary\n\n"
    
    for holding in holdings:
        stock_data = await get_stock_data(holding["ticker"])
        if not stock_data:
            continue
            
        news = await get_stock_news(stock_data["company_name"], holding["ticker"])
        
        content += f"\n{stock_data['company_name']} ({holding['ticker']})\n"
        content += f"Current Price: ${stock_data['current_price']}\n"
        content += f"Previous Close: ${stock_data['previous_close']}\n"
        content += f"Day Range: ${stock_data['day_low']} - ${stock_data['day_high']}\n"
        content += f"Your Position: {holding['amount']} shares\n"
        
        if news:
            content += "\nRecent News:\n"
            for article in news[:2]:
                content += f"- {article['title']}\n  {article['url']}\n"
        
        content += "\n" + "-"*50 + "\n"
    
    message = MessageSchema(
        subject=f"Daily Portfolio Summary - {datetime.now().strftime('%Y-%m-%d')}",
        recipients=[email],
        body=content,
        subtype="plain"
    )
    
    await fastmail.send_message(message)
