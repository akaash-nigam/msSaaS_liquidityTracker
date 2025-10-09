# Global Liquidity Tracker

A comprehensive web application for tracking and analyzing global liquidity based on Michael Howell's research in "Capital Wars: The Rise of Global Liquidity".

## Overview

This application tracks the $176+ trillion global liquidity cycle by aggregating central bank balance sheet data and providing real-time insights into market conditions.

## Features

- **Global Liquidity Index (GLI)** - Real-time calculation from 11+ central banks
- **Interactive Charts** - Visualize 10+ years of liquidity data
- **Cycle Analysis** - Track the 65-month liquidity cycle
- **Asset Correlations** - Compare GLI with stocks, crypto, commodities
- **Component Breakdown** - See individual central bank contributions

## Tech Stack

### Frontend
- Next.js 14+ (React with TypeScript)
- Tailwind CSS + shadcn/ui
- Recharts for data visualization
- SWR for data fetching

### Backend
- FastAPI (Python)
- PostgreSQL + TimescaleDB
- Redis for caching
- SQLAlchemy ORM

## Project Structure

```
liquidityTracker/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── docs/              # Documentation
├── PRD.md            # Product Requirements Document
└── README.md         # This file
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

Coming soon...

## Documentation

See [PRD.md](./PRD.md) for detailed product requirements and architecture.

## License

MIT

## Credits

Based on research by Michael J. Howell and CrossBorder Capital.
