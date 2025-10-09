# Global Liquidity Tracker - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+ (optional for MVP - app works with mock data)
- **Redis** 7+ (optional for MVP)
- **Git**

## Quick Start (Without Database)

For a quick demo using mock data, you don't need PostgreSQL or Redis:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd liquidityTracker
```

### 2. Set Up Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

### 3. Set Up Backend (in a new terminal)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The backend API will be available at http://localhost:8000

### 4. View the Application

Open your browser to http://localhost:3000 and you'll see the Global Liquidity Tracker dashboard with mock data!

---

## Full Setup (With Database & Real Data)

### Step 1: Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Install TimescaleDB Extension

```bash
# macOS
brew tap timescale/tap
brew install timescaledb

# Ubuntu
sudo add-apt-repository ppa:timescale/timescaledb-ppa
sudo apt update
sudo apt install timescaledb-2-postgresql-15
```

Configure TimescaleDB:
```bash
sudo timescaledb-tune
```

### Step 3: Create Database

```bash
# Login to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE liquidity_tracker;
CREATE USER liquidity_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE liquidity_tracker TO liquidity_user;

# Connect to the database
\c liquidity_tracker

# Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

# Exit psql
\q
```

### Step 4: Install Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

### Step 5: Get FRED API Key (Free)

1. Go to https://fred.stlouisfed.org/
2. Create a free account
3. Request an API key at https://fred.stlouisfed.org/docs/api/api_key.html
4. You'll receive your API key instantly

### Step 6: Configure Backend

```bash
cd backend

# Copy example env file
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your preferred editor
```

Update `.env` with your settings:
```env
DATABASE_URL=postgresql://liquidity_user:your_secure_password@localhost:5432/liquidity_tracker
REDIS_URL=redis://localhost:6379
FRED_API_KEY=your_fred_api_key_here
DEBUG=True
ENVIRONMENT=development
```

### Step 7: Initialize Database

```bash
# Activate virtual environment
source venv/bin/activate

# Run database initialization script
python -c "from app.database import init_db; init_db()"
```

### Step 8: Ingest Initial Data

```bash
# Run data ingestion to fetch Fed data
python scripts/ingest_data.py
```

This will:
- Fetch Federal Reserve balance sheet data
- Fetch Treasury General Account (TGA) data
- Fetch Reverse Repo (RRP) data
- Calculate and store GLI values

### Step 9: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Watch logs (optional):**
```bash
tail -f backend/logs/app.log
```

### Step 10: Verify Installation

1. **Check Backend Health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check GLI Endpoint:**
   ```bash
   curl http://localhost:8000/api/v1/gli/current
   ```

3. **Open Frontend:**
   Navigate to http://localhost:3000

---

## Development Workflow

### Running Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

### Code Formatting

**Backend:**
```bash
cd backend
black app/
```

**Frontend:**
```bash
cd frontend
npm run lint
```

### Database Migrations

When you make changes to models:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

---

## Scheduled Data Updates

To automatically update data daily, set up a cron job:

```bash
# Edit crontab
crontab -e

# Add this line to run at 7 PM daily (after Fed data release)
0 19 * * * cd /path/to/liquidityTracker/backend && /path/to/venv/bin/python scripts/ingest_data.py
```

---

## Troubleshooting

### Frontend won't start
- Make sure you're in the `frontend` directory
- Delete `node_modules` and `.next`, then run `npm install` again
- Check that port 3000 is not in use: `lsof -i :3000`

### Backend won't start
- Verify Python version: `python --version` (should be 3.11+)
- Check that virtual environment is activated
- Verify all dependencies installed: `pip list`
- Check port 8000: `lsof -i :8000`

### Database connection errors
- Verify PostgreSQL is running: `brew services list` or `systemctl status postgresql`
- Check database credentials in `.env`
- Test connection: `psql -U liquidity_user -d liquidity_tracker`

### FRED API errors
- Verify API key is correct in `.env`
- Check you haven't exceeded rate limits (no limits for basic tier)
- Test manually: `curl "https://api.stlouisfed.org/fred/series?series_id=WALCL&api_key=YOUR_KEY&file_type=json"`

### No data showing in frontend
- Check backend is running and healthy: `curl http://localhost:8000/health`
- Verify data was ingested: `curl http://localhost:8000/api/v1/gli/current`
- Check browser console for errors (F12)
- Verify CORS settings in backend

---

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment instructions.

---

## Need Help?

- Check the [FAQ](./FAQ.md)
- Review the [API Documentation](./API.md)
- Open an issue on GitHub
- Contact: support@liquiditytracker.com
