# API Keys Guide

## What API Keys Do You Need?

### For MVP (Current Version)

You only need **ONE** API key to get started with real data:

#### 1. FRED API Key (Federal Reserve Economic Data) - **FREE**

**What it's for:**
- Federal Reserve balance sheet data
- Treasury General Account (TGA)
- Reverse Repo Agreements (RRP)

**How to get it (takes 2 minutes):**

1. Go to https://fred.stlouisfed.org/
2. Click "My Account" → "Create New Account"
3. Fill in basic info (name, email)
4. Verify your email
5. Go to https://fred.stlouisfed.org/docs/api/api_key.html
6. Click "Request API Key"
7. Fill out the simple form
8. **You'll get your API key instantly!**

**Limits:**
- ✅ **Completely FREE**
- ✅ No rate limits for basic usage
- ✅ Unlimited historical data access

**Example key format:**
```
abcdef1234567890abcdef1234567890
```

---

## How to Add Your API Key

### Step 1: Create `.env` file

```bash
cd backend
cp .env.example .env
```

### Step 2: Edit `.env` file

Open `backend/.env` and add your key:

```bash
# Database (optional for MVP)
DATABASE_URL=postgresql://user:password@localhost:5432/liquidity_tracker
REDIS_URL=redis://localhost:6379

# FRED API Key - ADD YOUR KEY HERE
FRED_API_KEY=your_actual_key_here

# Application
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here

# CORS
ALLOWED_ORIGINS=http://localhost:3001,http://localhost:3002
```

### Step 3: Test it

```bash
cd backend
source venv/bin/activate
python -c "from app.config import settings; print(f'FRED Key: {settings.FRED_API_KEY[:10]}...')"
```

---

## Future API Keys (Phase 2+)

These are **NOT needed now**, but will be added in future phases:

### 2. ECB Statistical Data Warehouse - **FREE**
- For European Central Bank data
- Required in Phase 2
- Get from: https://data.ecb.europa.eu/

### 3. Bank of Japan Statistics - **FREE**
- For BOJ balance sheet data
- Required in Phase 2
- Get from: https://www.stat-search.boj.or.jp/

### 4. People's Bank of China - **May require translation**
- For PBoC data
- Required in Phase 2
- Get from: http://www.pbc.gov.cn/

### 5. Other Central Banks (Phase 2-3)
- Bank of England: https://www.bankofengland.co.uk/statistics
- Bank of Canada: https://www.bankofcanada.ca/
- Reserve Bank of Australia: https://www.rba.gov.au/
- Reserve Bank of India: https://rbi.org.in/
- Swiss National Bank: https://data.snb.ch/

---

## Do I Need a Database?

**Short answer: NO (for demo)**

The app works perfectly with **mock data** without any database or API keys!

**To use real data, you need:**

1. ✅ **FRED API Key** (free, instant)
2. ✅ **PostgreSQL** (free, 5-min install)

That's it for MVP!

---

## Quick Setup with FRED Data

### Option 1: Mac (Homebrew)

```bash
# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Create database
psql postgres -c "CREATE DATABASE liquidity_tracker;"
psql postgres -c "CREATE USER liquidity_user WITH PASSWORD 'password123';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE liquidity_tracker TO liquidity_user;"

# Update backend/.env
cd backend
cp .env.example .env
# Edit .env:
# FRED_API_KEY=your_key_here
# DATABASE_URL=postgresql://liquidity_user:password123@localhost:5432/liquidity_tracker

# Initialize and load data
python scripts/init_database.py
python scripts/ingest_data.py

# Start the app
python main.py
```

### Option 2: Docker (Alternative)

```bash
# Start PostgreSQL with Docker
docker run -d \
  --name liquidity-postgres \
  -e POSTGRES_PASSWORD=password123 \
  -e POSTGRES_DB=liquidity_tracker \
  -p 5432:5432 \
  postgres:15

# Continue with backend setup above
```

---

## Testing Your Setup

### 1. Test FRED API Connection

```bash
cd backend
source venv/bin/activate
python -c "
from app.services.fred_service import FREDService
import asyncio

async def test():
    service = FREDService()
    data = await service.fetch_fed_balance_sheet()
    print(f'✅ Got {len(data)} data points from FRED!')
    if data:
        print(f'Latest: {data[-1]}')

asyncio.run(test())
"
```

### 2. Test Database Connection

```bash
psql postgresql://liquidity_user:password123@localhost:5432/liquidity_tracker -c "SELECT COUNT(*) FROM central_bank_data;"
```

### 3. Test Full Pipeline

```bash
cd backend
python scripts/ingest_data.py --days 30
```

You should see:
```
📥 Fetching Federal Reserve data from FRED...
✅ success: 90 records added
🧮 Calculating Global Liquidity Index...
✅ success: 30 GLI records calculated
```

---

## Cost Breakdown

| Service | Cost | Required? |
|---------|------|-----------|
| FRED API | **FREE** | ✅ Yes (for real data) |
| PostgreSQL | **FREE** (self-hosted) | ✅ Yes (for real data) |
| Redis | **FREE** (self-hosted) | ⚠️ Optional (caching) |
| ECB Data | **FREE** | ❌ Phase 2 |
| BOJ Data | **FREE** | ❌ Phase 2 |
| PBoC Data | **FREE** | ❌ Phase 2 |

**Total cost for MVP: $0** 🎉

---

## Security Best Practices

### ✅ DO:
- Store API keys in `.env` file
- Add `.env` to `.gitignore` (already done)
- Use environment variables in production
- Rotate keys periodically

### ❌ DON'T:
- Commit API keys to git
- Share keys publicly
- Hard-code keys in source files
- Use production keys in development

---

## Troubleshooting

### "FRED API key not configured"
- Check `backend/.env` exists
- Verify `FRED_API_KEY=your_key` is set
- Restart backend server after adding key

### "No observations found"
- FRED may have updated series IDs
- Check https://fred.stlouisfed.org/series/WALCL
- Verify your key is active

### "Database connection failed"
- Check PostgreSQL is running: `brew services list`
- Test connection: `psql postgresql://liquidity_user:password123@localhost:5432/liquidity_tracker`
- Verify DATABASE_URL in `.env`

---

## Summary

**To get started with REAL data, you only need:**

1. Get FRED API key (2 minutes, free): https://fred.stlouisfed.org/
2. Install PostgreSQL (5 minutes, free)
3. Add key to `backend/.env`
4. Run `python scripts/ingest_data.py`

**That's it!** You'll have real Federal Reserve data powering your Global Liquidity Tracker.

No credit card, no paid services, no complex setup required! 🚀
