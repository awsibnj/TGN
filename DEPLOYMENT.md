# Deployment Guide

This guide covers deploying the WorkHub Telegram Bot to various platforms.

## Deployment Options

### 1. Local Machine (Development)

Best for testing and development.

```bash
# Run the bot
python bot.py

# Keep running in background (Linux/Mac)
nohup python bot.py > bot.log 2>&1 &

# Or use screen
screen -S workhub-bot
python bot.py
# Ctrl+A, D to detach
```

### 2. VPS (Ubuntu/Debian)

Recommended for production use.

#### Initial Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install git
sudo apt install git -y

# Clone/upload your bot files
git clone your-repository-url
cd telegram-workhub-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
nano .env
# Paste your configuration and save (Ctrl+X, Y, Enter)
```

#### Run with systemd (Recommended)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/workhub-bot.service
```

Add the following content:

```ini
[Unit]
Description=WorkHub Telegram Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/telegram-workhub-bot
Environment="PATH=/path/to/telegram-workhub-bot/venv/bin"
ExecStart=/path/to/telegram-workhub-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace:
- `your-username` with your Linux username
- `/path/to/telegram-workhub-bot` with actual path

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable workhub-bot

# Start the service
sudo systemctl start workhub-bot

# Check status
sudo systemctl status workhub-bot

# View logs
sudo journalctl -u workhub-bot -f
```

Manage the service:

```bash
# Stop the bot
sudo systemctl stop workhub-bot

# Restart the bot
sudo systemctl restart workhub-bot

# View logs
sudo journalctl -u workhub-bot -n 100
```

### 3. Heroku

Free tier available, good for small-scale deployment.

#### Setup

1. Install Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Login to Heroku:
```bash
heroku login
```

3. Create Procfile:
```bash
echo "worker: python bot.py" > Procfile
```

4. Create runtime.txt:
```bash
echo "python-3.9.16" > runtime.txt
```

5. Initialize git and deploy:
```bash
git init
heroku create your-app-name
git add .
git commit -m "Initial commit"
git push heroku main
```

6. Set environment variables:
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set SUPABASE_URL=your_url
heroku config:set SUPABASE_KEY=your_key
heroku config:set TELEGRAM_CHANNEL_ID=@yourchannel
heroku config:set TELEGRAM_CHANNEL_NAME="Your Channel Name"
heroku config:set ADMIN_TELEGRAM_UID=your_user_id
```

7. Scale the worker:
```bash
heroku ps:scale worker=1
```

8. View logs:
```bash
heroku logs --tail
```

### 4. Railway

Modern alternative to Heroku with better free tier.

#### Setup

1. Visit [Railway.app](https://railway.app) and sign up

2. Create new project → Deploy from GitHub

3. Add environment variables in Railway dashboard:
   - TELEGRAM_BOT_TOKEN
   - SUPABASE_URL
   - SUPABASE_KEY
   - TELEGRAM_CHANNEL_ID
   - TELEGRAM_CHANNEL_NAME
   - ADMIN_TELEGRAM_UID

4. Add Procfile (if not detected):
```
worker: python bot.py
```

5. Deploy and monitor logs in Railway dashboard

### 5. Docker

Containerized deployment for any platform.

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Create `.dockerignore`:

```
.env
.git
.gitignore
venv/
__pycache__/
*.pyc
*.log
README.md
DEPLOYMENT.md
```

Build and run:

```bash
# Build image
docker build -t workhub-bot .

# Run container
docker run -d \
  --name workhub-bot \
  --env-file .env \
  --restart unless-stopped \
  workhub-bot

# View logs
docker logs -f workhub-bot

# Stop container
docker stop workhub-bot

# Start container
docker start workhub-bot

# Remove container
docker rm workhub-bot
```

### 6. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: workhub-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
```

Run:

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Production Checklist

### Before Deployment

- [ ] Test all features locally
- [ ] Verify Supabase connection
- [ ] Test channel verification
- [ ] Verify wallet operations
- [ ] Test file uploads
- [ ] Check admin functions
- [ ] Set strong passwords
- [ ] Configure proper .gitignore

### Security

- [ ] Never commit `.env` file
- [ ] Use environment variables for secrets
- [ ] Enable Supabase RLS (Row Level Security)
- [ ] Limit Supabase API key permissions
- [ ] Set up Supabase backup schedule
- [ ] Monitor error logs
- [ ] Implement rate limiting (if needed)

### Monitoring

- [ ] Set up log rotation
- [ ] Monitor bot uptime
- [ ] Track error rates
- [ ] Monitor Supabase usage
- [ ] Set up alerts for critical errors

### Backup

```bash
# Backup Supabase data
# Go to Supabase Dashboard → Database → Backups

# Backup bot files
tar -czf workhub-bot-backup-$(date +%Y%m%d).tar.gz \
  --exclude=venv \
  --exclude=__pycache__ \
  --exclude=*.log \
  /path/to/telegram-workhub-bot
```

## Scaling Considerations

### Performance Tips

1. **Database Indexing**: Already included in schema
2. **Connection Pooling**: Consider using Supabase connection pooler
3. **Caching**: Implement Redis for frequent queries
4. **Rate Limiting**: Add rate limits for API calls
5. **Load Balancing**: Run multiple bot instances with webhook mode

### High Availability

For critical deployments:

1. Use multiple servers with load balancer
2. Set up Supabase replication
3. Implement health checks
4. Use managed database backups
5. Monitor with tools like Prometheus/Grafana

## Troubleshooting Deployment

### Bot Not Starting

```bash
# Check Python version
python --version

# Check dependencies
pip list

# Test database connection
python -c "from database import supabase; print(supabase.table('users').select('*').limit(1).execute())"
```

### Permission Errors

```bash
# Fix file permissions
chmod +x bot.py

# Fix directory permissions
chmod -R 755 /path/to/bot
```

### Memory Issues

```bash
# Monitor memory usage
htop
# or
ps aux | grep python

# Limit memory in systemd
# Add to [Service] section:
MemoryLimit=512M
```

### Connection Timeouts

- Check firewall settings
- Verify Supabase is accessible
- Test network connectivity
- Check API rate limits

## Updating the Bot

```bash
# Pull latest changes
git pull

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart workhub-bot

# Or with Docker
docker-compose down && docker-compose up -d --build
```

## Rollback Strategy

```bash
# With git
git log --oneline
git checkout <previous-commit-hash>
sudo systemctl restart workhub-bot

# With Docker
docker tag workhub-bot:latest workhub-bot:backup
docker-compose down
docker-compose up -d
```

## Support

For deployment issues:
1. Check bot logs: `sudo journalctl -u workhub-bot -n 100`
2. Verify environment variables: `printenv | grep TELEGRAM`
3. Test Supabase connection
4. Check Telegram API status
5. Review systemd service status

---

**Good luck with your deployment! 🚀**
