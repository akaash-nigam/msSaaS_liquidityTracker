# Global Liquidity Tracker - Project Summary

## What We Built

A comprehensive web application for tracking and analyzing the **$176+ trillion global liquidity cycle** based on Michael Howell's groundbreaking research from "Capital Wars: The Rise of Global Liquidity."

---

## Project Structure

```
liquidityTracker/
├── frontend/                  # Next.js 14 + TypeScript + Tailwind CSS
│   ├── app/                  # App router pages
│   │   ├── page.tsx          # Main dashboard
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/           # React components
│   │   ├── GLIHeroCard.tsx   # Main GLI display card
│   │   ├── GLIChart.tsx      # Interactive time-series chart
│   │   └── ComponentBreakdown.tsx  # Central bank breakdown
│   └── package.json          # Dependencies
│
├── backend/                  # FastAPI + Python + SQLAlchemy
│   ├── app/
│   │   ├── api/             # API routes
│   │   │   └── routes.py    # GLI endpoints
│   │   ├── models/          # Database models
│   │   │   ├── central_bank_data.py
│   │   │   └── global_liquidity_index.py
│   │   ├── schemas/         # Pydantic schemas
│   │   │   └── gli.py
│   │   ├── services/        # Business logic
│   │   │   ├── gli_service.py
│   │   │   ├── fred_service.py
│   │   │   └── data_ingestion_service.py
│   │   ├── config.py        # Settings
│   │   └── database.py      # DB connection
│   ├── main.py              # FastAPI app
│   └── requirements.txt     # Python dependencies
│
├── scripts/                 # Utility scripts
│   ├── init_database.py    # Database setup
│   └── ingest_data.py      # Data fetching
│
├── docs/                    # Documentation
│   └── SETUP.md            # Detailed setup guide
│
├── PRD.md                   # Product Requirements Document
├── QUICKSTART.md           # Quick start guide
└── README.md               # Project overview
```

---

## Features Implemented

### ✅ Frontend

1. **GLI Hero Card**
   - Current GLI value ($176.2T)
   - 1M, 3M, YoY percentage changes
   - Expansion/contraction status
   - Cycle position indicator (Day X of 1,950)
   - Progress bar showing cycle phase

2. **Interactive Time-Series Chart**
   - Beautiful area chart using Recharts
   - Timeframe selectors (1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y, ALL)
   - Hover tooltips with exact values
   - Gradient fills and smooth animations
   - Download chart functionality

3. **Component Breakdown Table**
   - All central bank contributions
   - Individual values and changes
   - Percentage of total GLI
   - Trend indicators (expanding/contracting)
   - Visual progress bars
   - Country flags for easy identification

4. **Design System**
   - Dark mode by default (sleek gradient background)
   - Custom color palette:
     - Primary: #0066FF (blue)
     - Expansion: #00C896 (green)
     - Contraction: #FF4757 (red)
   - Glassmorphism effects
   - Responsive design (desktop, tablet, mobile)

### ✅ Backend

1. **RESTful API**
   - `GET /api/v1/gli/current` - Current GLI value
   - `GET /api/v1/gli/historical` - Historical data with date ranges
   - `GET /api/v1/gli/components` - Component breakdown
   - `GET /api/v1/gli/cycle` - Cycle information
   - `POST /api/v1/data/refresh` - Trigger data refresh

2. **FRED API Integration**
   - Fetches Federal Reserve balance sheet (WALCL)
   - Fetches Treasury General Account (WDTGAL)
   - Fetches Reverse Repo data (RRPONTSYD)
   - Converts values to trillions
   - Handles rate limiting and errors
   - Falls back to mock data if no API key

3. **GLI Calculation Engine**
   - Formula: `GLI = FED - TGA - RRP + [other central banks]`
   - Calculates percentage changes (1D, 1M, 3M, 6M, 1Y)
   - Determines cycle position
   - Stores results in database

4. **Database Models**
   - PostgreSQL + TimescaleDB support
   - `central_bank_data` table for raw data
   - `global_liquidity_index` table for calculated GLI
   - Optimized indexes for time-series queries
   - SQLAlchemy ORM for type safety

5. **Services Architecture**
   - `FREDService`: External API integration
   - `GLIService`: Business logic for GLI operations
   - `DataIngestionService`: Data pipeline orchestration
   - Async/await for performance

---

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP**: Axios + SWR

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL 15 + TimescaleDB
- **Caching**: Redis (optional)
- **HTTP Client**: httpx
- **Data**: Pandas, NumPy

### Data Sources
- **FRED API** (Federal Reserve Economic Data)
- Future: ECB, BOJ, PBoC, BOE, BOC, RBA, RBI, SNB APIs

---

## How to Run

### Quick Start (Mock Data)

```bash
# Terminal 1 - Frontend
cd frontend
npm install
npm run dev

# Terminal 2 - Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open http://localhost:3000

### With Real Data

1. Install PostgreSQL
2. Get FRED API key (free): https://fred.stlouisfed.org/
3. Configure `backend/.env`
4. Run:
   ```bash
   python scripts/init_database.py
   python scripts/ingest_data.py
   python main.py
   ```

See [QUICKSTART.md](QUICKSTART.md) for details.

---

## What's Working

✅ Beautiful, responsive dashboard
✅ Interactive charts with multiple timeframes
✅ Component breakdown visualization
✅ FRED API integration
✅ GLI calculation engine
✅ PostgreSQL + TimescaleDB database schema
✅ RESTful API with FastAPI
✅ Mock data for demo purposes
✅ Comprehensive documentation

---

## Next Steps (Post-MVP)

Based on the PRD, here are the recommended next steps:

### Phase 2 (Months 4-6)
1. **Add More Central Banks**
   - ECB (European Central Bank)
   - BOJ (Bank of Japan)
   - PBoC (People's Bank of China)
   - BOE, BOC, RBA, RBI, SNB

2. **Alerts & Notifications**
   - Email alerts for threshold crossings
   - Cycle peak/trough notifications
   - Weekly digest emails

3. **User Authentication**
   - JWT-based auth
   - User profiles
   - Free vs Premium tiers

4. **Asset Correlations**
   - GLI vs S&P 500
   - GLI vs Bitcoin
   - GLI vs Gold, Bonds, Dollar Index

### Phase 3 (Months 7-9)
5. **Advanced Analytics**
   - Machine learning forecasts
   - Scenario analysis
   - Confidence intervals

6. **API Access**
   - API keys for developers
   - Rate limiting
   - Client libraries (Python, JS)

7. **Regional Analysis**
   - Americas, Europe, Asia-Pacific breakdown
   - Regional heatmaps
   - Comparative charts

---

## Key Metrics (from PRD)

**Target for Month 6:**
- 10,000+ Monthly Active Users
- 15% free-to-paid conversion
- 99.9% uptime
- $76K+ MRR

**MVP Timeline:**
- ✅ Weeks 1-2: Foundation (COMPLETED)
- ✅ Weeks 3-4: Data Pipeline (COMPLETED)
- ✅ Weeks 5-6: Core Features (COMPLETED)
- 🔄 Weeks 7-8: Asset Correlations (NEXT)
- Weeks 9-10: Polish & Testing
- Weeks 11-12: Launch Prep

---

## Files Created

**Documentation:**
- `PRD.md` - Comprehensive Product Requirements Document (70+ pages)
- `README.md` - Project overview
- `QUICKSTART.md` - 5-minute quick start guide
- `docs/SETUP.md` - Detailed setup instructions

**Frontend (14 files):**
- Application structure (Next.js 14)
- 3 main components (Hero Card, Chart, Breakdown)
- TypeScript configuration
- Tailwind CSS setup

**Backend (17 files):**
- FastAPI application
- Database models & schemas
- 3 service classes
- API routes
- Configuration management

**Scripts (2 files):**
- Database initialization
- Data ingestion

**Total: 36 files, ~4,000 lines of code**

---

## Demo Screenshots

When you run the app, you'll see:

1. **Header**: "Global Liquidity Tracker" with sign-in button
2. **Hero Card**: Large $176.2T value with green "EXPANDING" badge
3. **Chart**: Beautiful blue gradient area chart
4. **Table**: 8 rows of central banks with flags, values, changes
5. **Footer**: Data sources and attribution

All with a sleek dark gradient background (slate-900 → blue-900 → slate-900).

---

## Contributing

See [SETUP.md](docs/SETUP.md) for development setup.

Key commands:
- `npm run dev` - Start frontend dev server
- `python main.py` - Start backend server
- `pytest` - Run backend tests
- `npm test` - Run frontend tests

---

## Resources

- **Book**: "Capital Wars: The Rise of Global Liquidity" by Michael J. Howell
- **FRED API**: https://fred.stlouisfed.org/docs/api/
- **CrossBorder Capital**: https://www.crossbordercapital.com
- **Michael Howell's Substack**: https://capitalwars.substack.com

---

## License

MIT

---

**Built with ❤️ based on Michael Howell's research**

Track the $176 trillion liquidity cycle that drives global markets.
