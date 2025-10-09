# Product Requirements Document (PRD)
## Global Liquidity Tracker Application

**Version:** 1.0
**Date:** October 9, 2025
**Author:** Product Team
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Product Vision
Build a comprehensive web application that tracks and visualizes global liquidity in real-time, empowering investors, traders, and financial analysts to make data-driven decisions based on the $176+ trillion global liquidity cycle pioneered by Michael Howell's research.

### 1.2 Problem Statement
- Current global liquidity data is fragmented across multiple central bank sources
- No unified, real-time view of the liquidity cycle exists for retail investors
- Understanding liquidity's impact on asset prices requires deep financial expertise
- Expensive proprietary services (like CrossBorder Capital) are inaccessible to most users

### 1.3 Solution Overview
A web-based dashboard that aggregates central bank data, calculates the Global Liquidity Index (GLI), visualizes trends, and provides actionable insights for investment decisions.

### 1.4 Success Metrics
- **User Engagement:** 10,000+ monthly active users within 6 months
- **Data Accuracy:** 99.9% uptime with daily data refresh
- **User Satisfaction:** 4.5+ star rating
- **Conversion:** 15% free-to-premium conversion rate

---

## 2. User Personas

### 2.1 Primary Personas

#### Persona 1: "The Retail Investor"
- **Demographics:** 25-45 years old, tech-savvy, self-directed investor
- **Goals:** Understand macro trends to time market entries/exits
- **Pain Points:** Overwhelmed by fragmented data sources, lacks institutional tools
- **Use Case:** Check GLI weekly before making investment decisions in stocks/crypto

#### Persona 2: "The Professional Trader"
- **Demographics:** 30-50 years old, active day/swing trader
- **Goals:** Use liquidity as a leading indicator for risk-on/risk-off positioning
- **Pain Points:** Needs real-time alerts, wants API access for algorithmic trading
- **Use Case:** Monitor liquidity inflection points, integrate data into trading systems

#### Persona 3: "The Financial Analyst"
- **Demographics:** 28-55 years old, works at hedge fund/wealth management
- **Goals:** Generate market commentary and research reports
- **Pain Points:** Manually aggregating central bank data is time-consuming
- **Use Case:** Export charts and data for client presentations

### 2.2 Secondary Personas

#### Persona 4: "The Economics Student"
- **Demographics:** 20-30 years old, studying finance/economics
- **Goals:** Learn about global macro and liquidity cycles
- **Pain Points:** Educational resources lack real-time data
- **Use Case:** Study historical liquidity cycles and their market impacts

---

## 3. Core Features & Functionality

### 3.1 MVP Features (Phase 1)

#### Feature 1: Global Liquidity Index Dashboard
**Priority:** P0 (Must Have)

**Description:**
Real-time calculation and display of the Global Liquidity Index (GLI) using the formula:
```
GLI = FED - TGA - RRP + ECB + PBoC + BOJ + BOE + BOC + RBA + RBI + SNB
```

**User Stories:**
- As a user, I want to see the current GLI value prominently displayed
- As a user, I want to see the % change (daily, weekly, monthly, YoY)
- As a user, I want to see if liquidity is expanding or contracting

**Acceptance Criteria:**
- GLI updates daily at minimum (weekly for some components)
- Shows current value in trillions (e.g., "$176.2T")
- Color-coded: green for expansion, red for contraction
- Historical context: comparison to 1, 3, 6, 12 months ago

---

#### Feature 2: Interactive Time Series Chart
**Priority:** P0 (Must Have)

**Description:**
Zoomable, pannable chart showing GLI over time with cycle analysis

**User Stories:**
- As a user, I want to view GLI trends from 2008 to present
- As a user, I want to zoom into specific time periods
- As a user, I want to see cycle peaks and troughs marked
- As a user, I want to toggle between linear and log scale

**Acceptance Criteria:**
- Chart library supports 10+ years of historical data
- Timeframe selectors: 1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y, ALL
- Cycle annotations showing 65-month cycles
- Responsive design works on desktop and tablet

---

#### Feature 3: Component Breakdown View
**Priority:** P0 (Must Have)

**Description:**
Detailed view of individual components contributing to GLI

**User Stories:**
- As a user, I want to see each central bank's contribution
- As a user, I want to understand which regions are adding/reducing liquidity
- As a user, I want to see the Fed's balance sheet minus TGA and RRP

**Acceptance Criteria:**
- Table/chart showing all 11+ components
- Each component shows: current value, % change, contribution to total
- Visual breakdown (pie chart or stacked bar)
- Sortable by size or % change

**Components Table:**
| Component | Symbol | Source | Update Frequency |
|-----------|--------|--------|------------------|
| Federal Reserve Balance Sheet | FED | FRED: WALCL | Weekly |
| Treasury General Account | TGA | FRED: WDTGAL | Daily |
| Reverse Repo | RRP | FRED: RRPONTSYD | Daily |
| European Central Bank | ECB | ECB Data Portal | Weekly |
| People's Bank of China | PBoC | PBoC Statistics | Monthly |
| Bank of Japan | BOJ | BOJ Statistics | Weekly |
| Bank of England | BOE | BOE Statistics | Monthly |
| Bank of Canada | BOC | BOC Statistics | Monthly |
| Reserve Bank of Australia | RBA | RBA Statistics | Monthly |
| Reserve Bank of India | RBI | RBI Statistics | Bi-weekly |
| Swiss National Bank | SNB | SNB Statistics | Quarterly |

---

#### Feature 4: Liquidity Cycle Analysis
**Priority:** P1 (Should Have)

**Description:**
Visual representation of the 65-month liquidity cycle with projections

**User Stories:**
- As a user, I want to know where we are in the current cycle
- As a user, I want to see projected peak/trough dates
- As a user, I want historical cycles overlaid for comparison

**Acceptance Criteria:**
- Sine wave visualization showing cycle position
- Current cycle highlighted with "Days until peak/trough"
- Historical accuracy metrics for past cycle predictions
- Educational content explaining cycle methodology

---

#### Feature 5: Market Correlation Dashboard
**Priority:** P1 (Should Have)

**Description:**
Show correlation between GLI and major asset classes

**User Stories:**
- As a user, I want to see how GLI correlates with S&P 500
- As a user, I want to see GLI vs Bitcoin price
- As a user, I want to understand liquidity's impact on gold, bonds

**Acceptance Criteria:**
- Correlation coefficients for: SPX, BTC, Gold, 10Y Treasury, DXY
- Dual-axis charts showing GLI overlaid with each asset
- Correlation strength visualization (weak/moderate/strong)
- Lag analysis (does GLI lead or lag asset prices?)

**Asset Correlations to Track:**
- S&P 500 (SPX)
- Bitcoin (BTC)
- Gold (GLD)
- US 10-Year Treasury Yield
- US Dollar Index (DXY)
- Crude Oil (WTI)
- Real Estate (REITs)

---

### 3.2 Phase 2 Features (Post-MVP)

#### Feature 6: Custom Alerts & Notifications
**Priority:** P1 (Should Have)

**Description:**
Email/SMS/push alerts for liquidity inflection points

**User Stories:**
- As a user, I want alerts when GLI crosses specific thresholds
- As a user, I want notifications when cycle peaks are approaching
- As a user, I want weekly digest emails

**Acceptance Criteria:**
- Alert triggers: % change thresholds, absolute value thresholds, cycle events
- Multiple delivery methods: email, SMS, browser push
- Configurable frequency (real-time, daily, weekly)
- Alert history and management interface

---

#### Feature 7: Regional Liquidity Analysis
**Priority:** P2 (Nice to Have)

**Description:**
Breakdown of liquidity by geographic region (US, Europe, Asia, Emerging Markets)

**User Stories:**
- As a user, I want to compare US vs China liquidity trends
- As a user, I want to see which regions are leading liquidity expansion
- As a user, I want regional allocation recommendations

**Acceptance Criteria:**
- Regional aggregation: Americas, Europe, Asia-Pacific, Emerging Markets
- Heatmap visualization of regional liquidity changes
- Regional comparison charts
- Export regional data for analysis

---

#### Feature 8: Advanced Analytics & Forecasting
**Priority:** P2 (Nice to Have)

**Description:**
Machine learning models for liquidity forecasting

**User Stories:**
- As a user, I want 3-6 month GLI projections
- As a user, I want scenario analysis (QE/QT scenarios)
- As a user, I want confidence intervals for forecasts

**Acceptance Criteria:**
- 1-month, 3-month, 6-month forecasts
- Multiple models (time series, regression, ML ensemble)
- Forecast accuracy tracking
- Scenario builder for "what-if" analysis

---

#### Feature 9: API Access for Developers
**Priority:** P2 (Nice to Have)

**Description:**
RESTful API for programmatic access to GLI data

**User Stories:**
- As a developer, I want to fetch current GLI via API
- As a developer, I want historical data in JSON format
- As a developer, I want to build custom applications using GLI data

**Acceptance Criteria:**
- RESTful API with authentication (API keys)
- Endpoints: /current, /historical, /components, /correlations
- Rate limiting: 100 requests/hour (free), unlimited (premium)
- Comprehensive API documentation
- Client libraries (Python, JavaScript)

---

#### Feature 10: Educational Content Hub
**Priority:** P2 (Nice to Have)

**Description:**
Learning resources about global liquidity and investment strategies

**User Stories:**
- As a beginner, I want to learn what global liquidity is
- As a user, I want to understand how to use GLI for investing
- As a user, I want case studies of past liquidity cycles

**Acceptance Criteria:**
- Glossary of terms (QE, RRP, TGA, collateral, etc.)
- Video tutorials explaining liquidity concepts
- Blog with market commentary and analysis
- Case studies: 2008 crisis, 2020 COVID crash, 2022 tightening

---

### 3.3 Phase 3 Features (Future Enhancements)

#### Feature 11: Portfolio Integration
**Priority:** P3 (Future)

**Description:**
Connect user portfolios to receive personalized liquidity-based recommendations

**User Stories:**
- As a user, I want to see how my portfolio correlates with liquidity
- As a user, I want allocation recommendations based on cycle position
- As a user, I want risk scoring for current liquidity environment

---

#### Feature 12: Social/Community Features
**Priority:** P3 (Future)

**Description:**
Community discussions, analyst predictions, and sentiment tracking

**User Stories:**
- As a user, I want to see what other analysts are predicting
- As a user, I want to share my liquidity charts on social media
- As a user, I want to follow expert commentary

---

#### Feature 13: Mobile Application
**Priority:** P3 (Future)

**Description:**
Native iOS and Android apps for on-the-go monitoring

---

## 4. Data Architecture

### 4.1 Data Sources

#### Primary Sources (Free/Public)
1. **FRED API (St. Louis Fed)**
   - Endpoints: WALCL, WDTGAL, RRPONTSYD
   - Update Frequency: Daily/Weekly
   - Reliability: 99.9%+
   - API Limit: Unlimited (with API key)

2. **ECB Statistical Data Warehouse**
   - Balance sheet data
   - Update Frequency: Weekly
   - API: REST API available

3. **Bank for International Settlements (BIS)**
   - Global liquidity indicators
   - Update Frequency: Quarterly
   - Format: CSV downloads, API in development

4. **Individual Central Bank APIs**
   - BOJ, PBoC, BOE, BOC, RBA, RBI, SNB
   - Update Frequency: Varies (weekly to quarterly)
   - Format: Varies (APIs, CSV, XML)

#### Secondary Sources (Market Data)
5. **Alpha Vantage / Yahoo Finance API**
   - Asset price data (stocks, crypto, commodities)
   - For correlation analysis
   - Free tier: 500 requests/day

6. **CoinGecko API**
   - Cryptocurrency prices
   - Free tier: 10-50 requests/minute

### 4.2 Data Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Ingestion Layer                     │
├─────────────────────────────────────────────────────────────┤
│  - Scheduled jobs (cron) for each data source               │
│  - Rate limiting & retry logic                               │
│  - Data validation & cleansing                               │
│  - Error handling & alerting                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Data Storage Layer                         │
├─────────────────────────────────────────────────────────────┤
│  - PostgreSQL: Time-series data, user data, alerts          │
│  - TimescaleDB extension: Optimized time-series queries     │
│  - Redis: Caching layer for real-time dashboard             │
│  - S3/Object Storage: Historical data archives              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Calculation Engine                         │
├─────────────────────────────────────────────────────────────┤
│  - GLI calculation: FED - TGA - RRP + ECB + ... + SNB       │
│  - Rate of change calculations (%, YoY, MoM)                │
│  - Correlation analysis with assets                          │
│  - Cycle detection algorithms                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                               │
├─────────────────────────────────────────────────────────────┤
│  - REST API (Express.js/FastAPI)                            │
│  - GraphQL API (optional, for flexible queries)             │
│  - WebSocket: Real-time updates                              │
│  - Authentication: JWT tokens                                │
│  - Rate limiting per user tier                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Application                      │
├─────────────────────────────────────────────────────────────┤
│  - React/Next.js SPA                                        │
│  - Chart.js/Recharts/D3.js for visualizations              │
│  - Real-time updates via WebSocket                          │
│  - Responsive design (mobile/tablet/desktop)                │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Database Schema (Simplified)

#### Table: central_bank_data
```sql
CREATE TABLE central_bank_data (
  id SERIAL PRIMARY KEY,
  source VARCHAR(10) NOT NULL,  -- 'FED', 'ECB', 'BOJ', etc.
  indicator VARCHAR(50) NOT NULL,  -- 'balance_sheet', 'tga', 'rrp'
  date DATE NOT NULL,
  value NUMERIC(15,2) NOT NULL,
  currency VARCHAR(3) NOT NULL,  -- 'USD', 'EUR', 'JPY'
  unit VARCHAR(20),  -- 'billions', 'trillions'
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(source, indicator, date)
);

-- Hypertable for TimescaleDB optimization
SELECT create_hypertable('central_bank_data', 'date');
```

#### Table: global_liquidity_index
```sql
CREATE TABLE global_liquidity_index (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL UNIQUE,
  value NUMERIC(15,2) NOT NULL,  -- GLI in trillions USD
  change_pct NUMERIC(8,4),  -- % change from previous
  change_1m_pct NUMERIC(8,4),
  change_3m_pct NUMERIC(8,4),
  change_6m_pct NUMERIC(8,4),
  change_1y_pct NUMERIC(8,4),
  cycle_position VARCHAR(20),  -- 'expansion', 'peak', 'contraction', 'trough'
  created_at TIMESTAMP DEFAULT NOW()
);

SELECT create_hypertable('global_liquidity_index', 'date');
```

#### Table: asset_correlations
```sql
CREATE TABLE asset_correlations (
  id SERIAL PRIMARY KEY,
  asset_symbol VARCHAR(10) NOT NULL,  -- 'SPX', 'BTC', 'GLD'
  date DATE NOT NULL,
  asset_price NUMERIC(15,2) NOT NULL,
  gli_value NUMERIC(15,2) NOT NULL,
  correlation_30d NUMERIC(8,6),  -- 30-day rolling correlation
  correlation_90d NUMERIC(8,6),
  correlation_365d NUMERIC(8,6),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(asset_symbol, date)
);
```

#### Table: users
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  tier VARCHAR(20) DEFAULT 'free',  -- 'free', 'premium', 'enterprise'
  api_key VARCHAR(64) UNIQUE,
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP
);
```

#### Table: alerts
```sql
CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  alert_type VARCHAR(50) NOT NULL,  -- 'threshold', 'cycle_event', 'weekly_digest'
  condition JSONB NOT NULL,  -- Flexible JSON for different alert conditions
  delivery_method VARCHAR(20)[] DEFAULT ARRAY['email'],  -- ['email', 'sms', 'push']
  is_active BOOLEAN DEFAULT true,
  last_triggered TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.4 Data Update Schedule

| Data Source | Update Frequency | Scheduled Job Time (UTC) |
|-------------|------------------|--------------------------|
| FRED (FED, TGA, RRP) | Daily | 18:00 (after Fed release) |
| ECB | Weekly (Wednesday) | 10:00 Thursday |
| BOJ | Weekly (Thursday) | 08:00 Friday |
| PBoC | Monthly (15th) | 02:00 on 16th |
| BOE | Monthly (EOM) | 10:00 next day |
| BOC | Monthly (EOM) | 14:00 next day |
| RBA | Monthly (EOM) | 02:00 next day |
| RBI | Bi-weekly (Friday) | 12:00 Saturday |
| SNB | Quarterly | 09:00 day after release |
| Asset Prices | Daily | 22:00 (after US close) |
| GLI Calculation | Daily | 23:00 (after all updates) |

---

## 5. Technical Stack Recommendations

### 5.1 Frontend
- **Framework:** Next.js 14+ (React with SSR/SSG)
- **Language:** TypeScript
- **UI Library:** Tailwind CSS + shadcn/ui components
- **Charts:** Recharts (simple), D3.js (advanced custom visualizations)
- **State Management:** Zustand or React Context
- **API Client:** Axios or native fetch with SWR for caching
- **Real-time:** Socket.io-client for WebSocket connections

### 5.2 Backend
- **Framework:** Node.js with Express.js OR Python with FastAPI
  - **Recommendation:** FastAPI (Python) for better data science integration
- **Language:** TypeScript (Node) or Python 3.11+
- **ORM:** Prisma (Node) or SQLAlchemy (Python)
- **Task Queue:** Bull (Node) or Celery (Python) for scheduled jobs
- **Caching:** Redis
- **Authentication:** JWT with bcrypt for password hashing

### 5.3 Database
- **Primary DB:** PostgreSQL 15+
- **Extension:** TimescaleDB for time-series optimization
- **Caching:** Redis 7+
- **Object Storage:** AWS S3 or DigitalOcean Spaces (for archives)

### 5.4 Infrastructure
- **Hosting:**
  - **Option 1:** Vercel (frontend) + Railway/Render (backend)
  - **Option 2:** AWS (EC2, RDS, ElastiCache, S3)
  - **Option 3:** DigitalOcean App Platform (full stack)
- **CDN:** Cloudflare or Vercel Edge Network
- **Monitoring:** Sentry (errors), Datadog/Prometheus (metrics)
- **Logging:** Winston (Node) or Python logging → CloudWatch/Logstash

### 5.5 Development Tools
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions
- **Testing:** Jest (unit), Playwright (E2E)
- **Linting:** ESLint + Prettier (TS/JS), Black + Ruff (Python)
- **Documentation:** Swagger/OpenAPI for API docs
- **Project Management:** Linear or GitHub Projects

---

## 6. User Experience (UX) Design

### 6.1 Information Architecture

```
Home (Dashboard)
├── Global Liquidity Index Overview
│   ├── Current GLI Value (hero metric)
│   ├── % Change indicators
│   └── Expansion/Contraction status
├── Interactive Chart
│   ├── Time series visualization
│   ├── Cycle annotations
│   └── Timeframe selectors
├── Component Breakdown
│   ├── Central bank contributions
│   └── Regional split
└── Quick Insights
    ├── Current cycle position
    └── Market correlations summary

Analysis
├── Liquidity Cycle
│   ├── 65-month cycle visualization
│   ├── Historical cycles
│   └── Projections
├── Market Correlations
│   ├── Stocks (SPX, NDX)
│   ├── Crypto (BTC, ETH)
│   ├── Commodities (Gold, Oil)
│   └── Currencies (DXY)
└── Regional Analysis (Phase 2)
    ├── Americas
    ├── Europe
    └── Asia-Pacific

Data & API (Phase 2)
├── API Documentation
├── Data Downloads (CSV, JSON)
└── API Key Management

Learn
├── What is Global Liquidity?
├── How to Use This Data
├── Cycle Methodology
└── Case Studies

Account (Phase 2)
├── Profile Settings
├── Alert Configuration
├── Subscription Management
└── Usage Statistics
```

### 6.2 Key UI Components

#### Component 1: GLI Hero Card
```
┌─────────────────────────────────────────────────┐
│  Global Liquidity Index                         │
│                                                 │
│  $176.2T                                        │
│  ↑ +2.4% (1M)  ↑ +5.1% (3M)  ↑ +7.8% (YoY)    │
│                                                 │
│  Status: 🟢 EXPANDING                           │
│  Cycle Position: Late Expansion (Day 1,842)    │
└─────────────────────────────────────────────────┘
```

#### Component 2: Main Time Series Chart
- Line chart with area fill
- Y-axis: GLI in trillions (auto-scaled)
- X-axis: Date (adaptive: days, months, or years based on zoom)
- Annotations: Cycle peaks (🔺), troughs (🔻)
- Tooltips: Hover to see exact date + value
- Controls: Zoom, pan, reset, download image

#### Component 3: Component Breakdown Table
```
┌──────────────┬──────────┬───────────┬──────────────┬─────────────┐
│ Central Bank │ Value    │ Change 1M │ % of Total   │ Trend       │
├──────────────┼──────────┼───────────┼──────────────┼─────────────┤
│ 🇺🇸 Fed Net  │ $6.8T    │ +$120B    │ 38.6%        │ ↑ Expanding │
│ 🇨🇳 PBoC     │ $5.2T    │ +$85B     │ 29.5%        │ ↑ Expanding │
│ 🇪🇺 ECB      │ $3.1T    │ -$20B     │ 17.6%        │ ↓ Shrinking │
│ 🇯🇵 BOJ      │ $1.9T    │ +$15B     │ 10.8%        │ ↑ Expanding │
│ ...          │ ...      │ ...       │ ...          │ ...         │
└──────────────┴──────────┴───────────┴──────────────┴─────────────┘
```

#### Component 4: Cycle Gauge
- Circular gauge showing 65-month cycle position
- Color gradient: Green (trough) → Yellow (mid) → Red (peak)
- "Days to Peak/Trough" countdown
- Historical accuracy indicator

#### Component 5: Correlation Cards
```
┌─────────────────────────┐  ┌─────────────────────────┐
│  S&P 500                │  │  Bitcoin                │
│  Correlation: 0.72 🟢   │  │  Correlation: 0.85 🟢   │
│  [Mini chart overlay]   │  │  [Mini chart overlay]   │
│  Strong Positive        │  │  Very Strong Positive   │
└─────────────────────────┘  └─────────────────────────┘
```

### 6.3 Color Scheme & Design System

**Brand Colors:**
- Primary: #0066FF (blue - representing liquidity flow)
- Secondary: #00C896 (teal - representing growth)
- Accent: #FF6B00 (orange - representing alerts/warnings)

**Data Visualization Colors:**
- Expansion: #00C896 (green)
- Contraction: #FF4757 (red)
- Neutral: #A4B0BE (gray)
- Positive correlation: #0066FF (blue)
- Negative correlation: #8B5CF6 (purple)

**Typography:**
- Headings: Inter (sans-serif)
- Body: Inter
- Monospace (numbers): JetBrains Mono

**Dark Mode Support:** Yes (with toggle)

---

## 7. Monetization Strategy

### 7.1 Tiered Pricing Model

#### Free Tier
- Current GLI value
- Daily updated charts (not real-time)
- Basic component breakdown
- 1-year historical data
- Weekly email digest
- Ads displayed

**Price:** $0/month

---

#### Premium Tier
- Everything in Free, plus:
- Real-time updates (hourly for faster-updating components)
- 10+ years historical data
- Advanced correlation analysis
- Custom alerts (up to 10)
- No ads
- CSV/JSON data exports
- Email + browser push notifications
- Priority support

**Price:** $19/month or $190/year (save 17%)

---

#### Pro Tier
- Everything in Premium, plus:
- API access (1,000 requests/day)
- Unlimited alerts
- Advanced forecasting models
- Regional liquidity breakdown
- SMS notifications
- Dedicated support
- White-label embeds for blogs/websites

**Price:** $49/month or $490/year (save 17%)

---

#### Enterprise Tier
- Everything in Pro, plus:
- Unlimited API access
- Custom data integrations
- SLA guarantee (99.9% uptime)
- Dedicated account manager
- Custom reporting
- On-premise deployment option
- Priority feature requests

**Price:** Custom (starting at $500/month)

---

### 7.2 Revenue Projections (Year 1)

**Assumptions:**
- 10,000 MAU by month 6
- 15% free-to-paid conversion
- 70% Premium, 25% Pro, 5% Enterprise (of paid users)

**Monthly Revenue (Month 12):**
- Free users: 8,500 (ad revenue ~$500/month)
- Premium: 1,050 × $19 = $19,950
- Pro: 375 × $49 = $18,375
- Enterprise: 75 × $500 = $37,500
- **Total MRR:** ~$76,325
- **Annual Run Rate:** ~$916,000

---

## 8. MVP Scope & Timeline

### 8.1 MVP Definition

**Included in MVP:**
- Global Liquidity Index calculation (11 components)
- Interactive time series chart (10 years of data)
- Component breakdown table/chart
- Basic cycle visualization
- Correlation with 5 assets (SPX, BTC, Gold, DXY, 10Y Treasury)
- Responsive web design
- User authentication (sign up, login)
- Free tier only

**Excluded from MVP:**
- Alerts & notifications
- API access
- Advanced forecasting
- Regional analysis
- Mobile apps
- Premium features
- Payment processing

### 8.2 Development Timeline

#### Week 1-2: Foundation
- [ ] Set up project repository
- [ ] Initialize Next.js frontend
- [ ] Initialize FastAPI backend
- [ ] Set up PostgreSQL + TimescaleDB
- [ ] Configure Redis
- [ ] Design database schema
- [ ] Create base UI components (header, footer, layout)

#### Week 3-4: Data Pipeline
- [ ] Implement FRED API integration (FED, TGA, RRP)
- [ ] Implement ECB API integration
- [ ] Implement other central bank scrapers/APIs
- [ ] Build data ingestion scheduler
- [ ] Create data validation & cleansing logic
- [ ] GLI calculation engine
- [ ] Store historical data (backfill from 2008)

#### Week 5-6: Core Features
- [ ] GLI dashboard (hero card, current value)
- [ ] Interactive time series chart (Recharts/D3)
- [ ] Component breakdown visualization
- [ ] Basic cycle detection & visualization
- [ ] Connect frontend to backend API

#### Week 7-8: Asset Correlations
- [ ] Integrate asset price APIs (Yahoo Finance, CoinGecko)
- [ ] Calculate correlations (30d, 90d, 365d)
- [ ] Build correlation dashboard UI
- [ ] Dual-axis charts (GLI vs assets)

#### Week 9-10: Polish & Testing
- [ ] Responsive design (mobile, tablet)
- [ ] Dark mode implementation
- [ ] User authentication (JWT)
- [ ] Error handling & loading states
- [ ] Unit tests (80% coverage target)
- [ ] E2E tests (critical user flows)
- [ ] Performance optimization (caching, lazy loading)

#### Week 11-12: Launch Prep
- [ ] Documentation (user guide, FAQ)
- [ ] SEO optimization (meta tags, sitemap)
- [ ] Analytics integration (Google Analytics, Mixpanel)
- [ ] Bug fixes & refinements
- [ ] Beta user testing (10-20 users)
- [ ] Deploy to production
- [ ] **MVP LAUNCH** 🚀

**Total MVP Timeline:** 12 weeks (3 months)

### 8.3 Post-MVP Roadmap

#### Q1 Post-Launch (Months 4-6)
- Alerts & notifications system
- Premium tier + payment integration (Stripe)
- API access for Pro tier
- User feedback collection & iteration
- Marketing & user acquisition campaigns

#### Q2 Post-Launch (Months 7-9)
- Regional liquidity analysis
- Advanced forecasting models
- Mobile app (React Native or PWA)
- Enterprise tier features
- Partnerships with financial content creators

#### Q3 Post-Launch (Months 10-12)
- Portfolio integration
- Social/community features
- Advanced analytics (AI/ML models)
- International expansion (multi-language)
- White-label solution for institutions

---

## 9. Risk Assessment & Mitigation

### 9.1 Technical Risks

**Risk 1: Data Source Reliability**
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:**
  - Implement redundant data sources where possible
  - Cache data with fallback to last known values
  - Monitor data quality with automated alerts
  - Build manual override capability

**Risk 2: API Rate Limits**
- **Impact:** Medium
- **Likelihood:** Medium
- **Mitigation:**
  - Implement intelligent caching (Redis)
  - Respect rate limits with exponential backoff
  - Consider paid tiers for critical APIs
  - Build data archives to reduce API calls

**Risk 3: Scalability**
- **Impact:** High
- **Likelihood:** Low (early stage)
- **Mitigation:**
  - Use TimescaleDB for time-series optimization
  - Implement CDN for static assets
  - Horizontal scaling architecture (containerized services)
  - Load testing before major user growth

### 9.2 Business Risks

**Risk 4: User Acquisition**
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:**
  - SEO optimization for "global liquidity" keywords
  - Content marketing (blog, YouTube explanations)
  - Partnerships with financial influencers
  - Free tier with generous features to build user base

**Risk 5: Competition**
- **Impact:** Medium
- **Likelihood:** Medium
- **Mitigation:**
  - Focus on superior UX (simpler, more intuitive than competitors)
  - Build community and educational content
  - Faster iteration based on user feedback
  - Unique features (forecasting, alerts, correlations)

**Risk 6: Regulatory Compliance**
- **Impact:** High
- **Likelihood:** Low
- **Mitigation:**
  - Include disclaimer: "Not financial advice"
  - Consult legal counsel for fintech regulations
  - GDPR compliance for EU users
  - SOC 2 certification for enterprise clients (future)

### 9.3 Operational Risks

**Risk 7: Data Accuracy Issues**
- **Impact:** Critical
- **Likelihood:** Low
- **Mitigation:**
  - Implement data validation at ingestion
  - Cross-reference multiple sources
  - Manual review for anomalies
  - Transparent methodology disclosure

**Risk 8: Key Person Dependency**
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:**
  - Comprehensive documentation
  - Code reviews and pair programming
  - Knowledge sharing sessions
  - Modular architecture for easier onboarding

---

## 10. Success Metrics & KPIs

### 10.1 Product Metrics

**Engagement Metrics:**
- Daily Active Users (DAU)
- Monthly Active Users (MAU)
- DAU/MAU ratio (target: >20% = sticky product)
- Average session duration (target: >3 minutes)
- Pages per session (target: >4)
- Bounce rate (target: <40%)

**Feature Adoption:**
- % users viewing cycle analysis
- % users exploring correlations
- % users downloading data
- % users setting up alerts (post-MVP)

**Retention:**
- D1, D7, D30 retention rates
- Cohort analysis (monthly cohorts)
- Churn rate (target: <5% monthly for paid users)

### 10.2 Business Metrics

**Revenue Metrics:**
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Average Revenue Per User (ARPU)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- LTV:CAC ratio (target: >3:1)
- Free-to-paid conversion rate (target: >15%)

**Growth Metrics:**
- Month-over-month user growth (target: >20%)
- Month-over-month revenue growth (target: >15%)
- Viral coefficient (referrals per user)
- Net Promoter Score (NPS) (target: >40)

### 10.3 Technical Metrics

**Performance:**
- Page load time (target: <2 seconds)
- API response time (target: <200ms for cached, <1s for computed)
- Uptime (target: 99.9%)
- Error rate (target: <0.1%)

**Data Quality:**
- Data freshness (hours since last update per source)
- Data completeness (% of expected data points received)
- Calculation accuracy (verified against manual calculations)

---

## 11. Open Questions & Decisions Needed

### 11.1 Technical Decisions

1. **Backend Language: Python (FastAPI) vs Node.js (Express)?**
   - **Recommendation:** Python for better data science libraries (pandas, numpy, scikit-learn)

2. **Chart Library: Recharts vs D3.js vs Chart.js?**
   - **Recommendation:** Recharts for MVP (simpler), D3.js for advanced features

3. **Deployment: Cloud provider?**
   - **Recommendation:** Start with Railway (simplicity) → migrate to AWS if scaling needs arise

4. **Real-time Updates: WebSocket vs Server-Sent Events vs Polling?**
   - **Recommendation:** Polling for MVP (simpler), WebSocket for Phase 2

### 11.2 Product Decisions

5. **Should we build mobile apps or prioritize web responsiveness?**
   - **Recommendation:** Web-first (responsive) for MVP, native apps in Phase 3

6. **How much free data should we give away?**
   - **Recommendation:** 1 year of history free, 10+ years for paid (aligns with competitor analysis)

7. **Should we partner with data providers (CrossBorder Capital) or build independently?**
   - **Recommendation:** Build independently with public data, explore partnerships later

8. **Educational content: In-house or hire finance writers?**
   - **Recommendation:** In-house for MVP (founder knowledge), hire writers post-launch

### 11.3 Business Decisions

9. **Launch strategy: Private beta vs public launch?**
   - **Recommendation:** Private beta (100 users) → iterate → public launch

10. **Geographic focus: US-first or global from day 1?**
    - **Recommendation:** Global from day 1 (data is global, audience is global)

11. **B2C vs B2B focus?**
    - **Recommendation:** B2C for MVP, B2B (enterprise) in Phase 2

---

## 12. Appendix

### 12.1 Competitor Analysis

| Competitor | Features | Pricing | Strengths | Weaknesses |
|------------|----------|---------|-----------|------------|
| CrossBorder Capital | Proprietary GLI, 90+ countries, professional research | $500+/month (institutional) | Most comprehensive, pioneer in field | Expensive, not retail-friendly |
| TradingView GLI Indicators | Community-built indicators, charting | $15-60/month | Integrated with trading platform | Less accurate, not dedicated to liquidity |
| MacroMicro | Economic charts incl. M2 aggregates | Free + Premium (~$30/month) | Clean UI, Asian market focus | Doesn't calculate true GLI, less analysis |
| **Our App** | **True GLI calculation, cycle analysis, correlations, alerts** | **$0-49/month** | **Retail-focused, educational, affordable** | **New player, building credibility** |

### 12.2 Glossary

- **GLI (Global Liquidity Index):** Aggregate measure of central bank balance sheets and money supply
- **TGA (Treasury General Account):** US government's account at the Federal Reserve (reduces private sector liquidity when funded)
- **RRP (Reverse Repo):** Fed facility where institutions park cash overnight (reduces circulating liquidity)
- **QE (Quantitative Easing):** Central bank asset purchases that expand balance sheet and increase liquidity
- **QT (Quantitative Tightening):** Central bank balance sheet reduction through asset sales or runoff
- **Collateral:** Assets pledged to secure loans (critical in liquidity framework)
- **Risk-On/Risk-Off:** Market regime characterized by appetite for risky assets vs flight to safety

### 12.3 References

- Howell, Michael J. (2020). *Capital Wars: The Rise of Global Liquidity*. Springer.
- CrossBorder Capital: https://www.crossbordercapital.com
- Federal Reserve Economic Data (FRED): https://fred.stlouisfed.org
- Bank for International Settlements: https://www.bis.org/statistics/gli.htm
- Michael Howell's Capital Wars Substack: https://capitalwars.substack.com

---

## Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-09 | Product Team | Initial draft |

---

**End of PRD**
