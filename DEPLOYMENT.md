# Deployment Guide

This guide covers deploying the Telegram Expense Bot to various platforms.

## Prerequisites

Before deploying, ensure you have:

1. **Telegram Bot Token** from @BotFather
2. **Ollama** for LLM integration (included automatically)
3. **PostgreSQL Database** (Supabase recommended)
4. **Public HTTPS URL** for webhook (required by Telegram)

## Quick Start with Docker Compose

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd darwin-ia-challenge
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your values
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Set up webhook:**
   ```bash
   # Replace with your public URL
   curl -X POST "http://localhost:8001/set-webhook" \
     -H "Content-Type: application/json" \
     -d '{"webhook_url": "https://your-domain.com/webhook"}'
   ```

## Production Deployment

### Option 1: Railway (Recommended)

Railway provides easy deployment with PostgreSQL support.

1. **Create Railway account** and connect your GitHub repository

2. **Set environment variables:**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
   DATABASE_URL=postgresql://...
   BOT_SERVICE_URL=https://your-bot-service.railway.app
   ```

3. **Deploy services:**
   - Deploy `bot-service` to Railway
   - Deploy `connector-service` to Railway
   - Set up PostgreSQL database in Railway

4. **Configure webhook:**
   ```bash
   curl -X POST "https://your-connector-service.railway.app/set-webhook" \
     -H "Content-Type: application/json" \
     -d '{"webhook_url": "https://your-connector-service.railway.app/webhook"}'
   ```

### Option 2: Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy each service:**
   ```bash
   # Deploy Bot Service
   cd bot-service
   vercel --prod
   
   # Deploy Connector Service
   cd ../connector-service
   vercel --prod
   ```

3. **Set environment variables** in Vercel dashboard

### Option 3: Heroku

1. **Install Heroku CLI**

2. **Create apps:**
   ```bash
   heroku create your-bot-service
   heroku create your-connector-service
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Set environment variables:**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   heroku config:set OLLAMA_BASE_URL=http://localhost:11434
heroku config:set OLLAMA_MODEL=llama2
   ```

## Database Setup

### Supabase (Recommended)

1. **Create Supabase project**
2. **Run the schema:**
   ```sql
   -- Copy and paste the contents of database/schema.sql
   ```
3. **Get connection string** from Supabase dashboard
4. **Update environment variables** with the connection string

### Other PostgreSQL Providers

- **Neon**: Serverless PostgreSQL
- **Railway**: Built-in PostgreSQL
- **Heroku**: PostgreSQL addon
- **AWS RDS**: Managed PostgreSQL

## Environment Variables

### Bot Service
```bash
DATABASE_URL=postgresql://username:password@host:port/database
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
BOT_SERVICE_PORT=8000
BOT_SERVICE_HOST=0.0.0.0
LOG_LEVEL=INFO
```

### Connector Service
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_SERVICE_URL=https://your-bot-service.com
CONNECTOR_SERVICE_PORT=8001
CONNECTOR_SERVICE_HOST=0.0.0.0
LOG_LEVEL=INFO
```

## Testing the Deployment

1. **Check health endpoints:**
   ```bash
   curl https://your-bot-service.com/health
   curl https://your-connector-service.com/health
   ```

2. **Test bot info:**
   ```bash
   curl https://your-connector-service.com/bot-info
   ```

3. **Send test message** to your Telegram bot

## Monitoring and Logs

### Railway
- View logs in Railway dashboard
- Monitor resource usage
- Set up alerts

### Vercel
- View function logs in Vercel dashboard
- Monitor performance metrics

### Heroku
```bash
heroku logs --tail -a your-app-name
```

## Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Consider implementing rate limiting
4. **Monitoring**: Set up monitoring and alerting
5. **Backups**: Regular database backups

## Troubleshooting

### Common Issues

1. **Webhook not receiving updates:**
   - Check webhook URL is HTTPS
   - Verify bot token is correct
   - Check webhook info: `GET /webhook-info`

2. **Database connection errors:**
   - Verify DATABASE_URL format
   - Check database is accessible
   - Ensure schema is applied

3. **Ollama errors:**
   - Verify API key is valid
   - Check API usage limits
   - Monitor API response times

### Debug Commands

```bash
# Check webhook status
curl https://your-connector-service.com/webhook-info

# Test bot service directly
curl -X POST https://your-bot-service.com/process-expense \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": "123456789", "message": "Pizza 20 bucks"}'

# Check database connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

## Scaling Considerations

1. **Database**: Use connection pooling
2. **Services**: Deploy multiple instances
3. **Caching**: Add Redis for caching
4. **CDN**: Use CDN for static assets
5. **Monitoring**: Set up comprehensive monitoring

## Cost Optimization

1. **Database**: Use appropriate tier for your needs
2. **Ollama**: Monitor model performance and memory usage
3. **Hosting**: Choose cost-effective hosting
4. **Caching**: Implement caching to reduce API calls 