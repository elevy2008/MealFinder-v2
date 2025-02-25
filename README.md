# Return - Stock Portfolio Backend

Backend service for the Return stock portfolio tracking application.

## Features

- User authentication and registration
- Portfolio management (add/remove holdings)
- Real-time stock data integration
- News aggregation for stocks
- Email notifications and summaries
- Rate limiting (5 requests/minute)
- Comprehensive error handling and logging

## Development

1. Install dependencies:
```bash
poetry install
```

2. Run development server:
```bash
poetry run uvicorn app.main:app --reload
```

## API Documentation

- `/auth/*` - Authentication endpoints
- `/portfolio/*` - Portfolio management
- `/email/*` - Email preferences and notifications

## Environment Variables

Required environment variables:
- `MAIL_USERNAME` - Email service username
- `MAIL_PASSWORD` - Email service password
- `MAIL_FROM` - Sender email address
- `MAIL_SERVER` - SMTP server address
- `MAIL_PORT` - SMTP server port (default: 587)

## Deployment

Deployed on Fly.io at https://app-jrgccxth.fly.dev
