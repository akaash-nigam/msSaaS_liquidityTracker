# 🚀 Starting the Global Liquidity Tracker

## Quick Start Commands

Since ports 3000 and 8000 are occupied, we're using **3001** and **8001**.

### Terminal 1 - Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:3001**

### Terminal 2 - Start Backend

```bash
cd backend

# Create and activate virtual environment (first time only)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
python main.py
```

Backend API will be available at: **http://localhost:8001**

---

## What You'll See

Once both servers are running, open **http://localhost:3001** in your browser:

1. ✨ Beautiful dark gradient dashboard
2. 📊 GLI Hero Card showing $176.2T with changes
3. 📈 Interactive time-series chart (1M, 3M, 6M, 1Y options)
4. 🏦 Central bank component breakdown table
5. 🔄 Cycle position indicator

---

## API Endpoints

Once backend is running, you can test:

- Health check: http://localhost:8001/health
- Current GLI: http://localhost:8001/api/v1/gli/current
- Historical: http://localhost:8001/api/v1/gli/historical?timeframe=1Y
- Components: http://localhost:8001/api/v1/gli/components
- API docs: http://localhost:8001/docs (Swagger UI)

---

## Using Mock Data vs Real Data

### Currently: Mock Data (Default)
The app works immediately with mock/demo data - **no database or API keys needed!**

### To Use Real FRED Data:

1. **Get a free FRED API key:**
   - Visit https://fred.stlouisfed.org/
   - Create account (free)
   - Get API key from https://fred.stlouisfed.org/docs/api/api_key.html

2. **Set up PostgreSQL:**
   ```bash
   # Install PostgreSQL (macOS)
   brew install postgresql@15
   brew services start postgresql@15

   # Create database
   psql postgres -c "CREATE DATABASE liquidity_tracker;"
   ```

3. **Configure backend:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add:
   # FRED_API_KEY=your_key_here
   # DATABASE_URL=postgresql://user:password@localhost:5432/liquidity_tracker
   ```

4. **Initialize and load data:**
   ```bash
   python scripts/init_database.py
   python scripts/ingest_data.py
   ```

---

## Troubleshooting

### Port already in use?
If you see "address already in use":

**Frontend:**
```bash
# Use a different port
cd frontend
npm run dev -- -p 3002  # Try 3002, 3003, etc.
```

**Backend:**
Edit `backend/main.py` and change port to 8002, 8003, etc.

### Frontend won't start?
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Backend errors?
```bash
cd backend
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Try running again
python main.py
```

### Browser shows blank page?
- Check browser console (F12) for errors
- Verify both frontend AND backend are running
- Try clearing browser cache (Cmd+Shift+R / Ctrl+Shift+F5)

---

## What Next?

1. **Explore the app** - Click different timeframes, view components
2. **Check API docs** - Visit http://localhost:8001/docs
3. **Read the PRD** - See PRD.md for complete feature roadmap
4. **Customize** - Edit components in `frontend/components/`
5. **Add real data** - Follow steps above to connect FRED API

---

## Need Help?

- 📖 Full setup guide: [docs/SETUP.md](docs/SETUP.md)
- 🎯 Quick start: [QUICKSTART.md](QUICKSTART.md)
- 📋 Project overview: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 📊 Product roadmap: [PRD.md](PRD.md)

---

**Enjoy tracking the $176 trillion global liquidity cycle! 🌊💰**
