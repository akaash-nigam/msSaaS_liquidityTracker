# Quick Start Guide

Get the Global Liquidity Tracker running in 5 minutes!

## Option 1: Quick Demo (No Database Required)

This gets you up and running immediately with mock data.

### Step 1: Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

### Step 2: Start the Backend (in a new terminal)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**That's it!** You now have a working Global Liquidity Tracker with mock data.

---

## Option 2: Full Setup (With Real FRED Data)

### Prerequisites
- PostgreSQL 15+ installed and running
- Get a free FRED API key from https://fred.stlouisfed.org/

### Step 1: Set Up Database

```bash
# Create database
psql postgres -c "CREATE DATABASE liquidity_tracker;"
psql postgres -c "CREATE USER liquidity_user WITH PASSWORD 'password123';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE liquidity_tracker TO liquidity_user;"
```

### Step 2: Configure Backend

```bash
cd backend
cp .env.example .env
# Edit .env and add your FRED_API_KEY
```

### Step 3: Initialize & Load Data

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create tables
python scripts/init_database.py

# Fetch data from FRED (last 365 days)
python scripts/ingest_data.py
```

### Step 4: Start Backend

```bash
python main.py
```

### Step 5: Start Frontend (in new terminal)

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000

---

## What You'll See

1. **Hero Card**: Current GLI value ($176.2T) with change indicators
2. **Interactive Chart**: Historical GLI trends with time period selection
3. **Component Breakdown**: Individual central bank contributions
4. **Cycle Analysis**: Where we are in the 65-month liquidity cycle

---

## API Endpoints

Once the backend is running:

- Health check: http://localhost:8000/health
- Current GLI: http://localhost:8000/api/v1/gli/current
- Historical data: http://localhost:8000/api/v1/gli/historical?timeframe=1Y
- Components: http://localhost:8000/api/v1/gli/components
- API docs: http://localhost:8000/docs

---

## Next Steps

- Read the full [Setup Guide](docs/SETUP.md)
- Review the [PRD](PRD.md) for feature roadmap
- Check [API Documentation](docs/API.md)
- Customize the dashboard components

## Troubleshooting

**Frontend won't start?**
- Verify you're in the `frontend` directory
- Run `rm -rf node_modules .next && npm install`

**Backend won't start?**
- Check Python version: `python --version` (need 3.11+)
- Activate venv: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**No data showing?**
- The app works with mock data by default
- For real data, configure FRED_API_KEY in .env
- Run `python scripts/ingest_data.py`

Need help? Check the [Setup Guide](docs/SETUP.md) or open an issue!
