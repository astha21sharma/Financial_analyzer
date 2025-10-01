# 📈 Financial Analyzer

A stock analysis tool that fetches historical & fundamental data for **US** and **Indian equities**, merges datasets, computes technical indicators, and highlights important patterns like **Golden Crossovers** & **Death Crossovers**.

---

## 1. Project Overview

This project provides a framework for analyzing stock performance by combining **price data** with **fundamentals**.  

**Features:**
- Fetch OHLCV & quarterly fundamental data from APIs  
- Handle **old/regular stocks** and **recent IPOs**  
- Compute indicators:  
  - 50-day & 200-day SMA  
  - 52-week high/low detection  
  - Golden & Death Crossovers  
- Calculate ratios:  
  - Price-to-Book (P/B)  
  - Book Value Per Share (BVPS)  
  - Enterprise Value (EV)  

---
## 📂 Project Structure

```
financial_analyzer/
├── financial_analyzer/
│   ├── __init__.py
│   ├── config.py
│   ├── data_fetcher.py
│   ├── database.py
│   ├── models.py
│   ├── processor.py
│   ├── signals.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_processor.py
│   └── test_signals.py
├── config.yaml.example
├── pyproject.toml
└── README.md
```

---
## 2. Setup Instructions

### 🔧 Prerequisites
- Python **3.9+**  
- [uv](https://docs.astral.sh/uv/) (for dependency management)  

### 📦 Installation

### Install
```bash
# Install dependencies
uv sync
````

### Config

Copy and edit config:

```bash
cp config.yaml.example config.yaml
```

Example `config.yaml`:

```yaml
database:
  path: "financial_data.db"

logging:
  level: "INFO"

data_settings:
  historical_period: "5y"
  min_trading_days_for_sma: 200
```

---

## ▶️ Usage

### Run pipeline

```bash
# US stock
uv run python -m financial_analyzer.main run --ticker NVDA --output nvda_analysis.json

# Indian stock
uv run python -m financial_analyzer.main run --ticker RELIANCE.NS --output reliance_analysis.json

# Recent IPO
uv run python -m financial_analyzer.main run --ticker SWIGGY.NS --output swiggy_analysis.json
```

---

## 4. Database Schema

The project uses an **SQLite database** with three main tables:

- **tickers**
  - Stores basic stock information.
  - Columns: `id` (PK), `ticker_symbol`, `company_name`, `exchange`, `market`.

- **daily_metrics**
  - Stores all calculated daily metrics for each ticker.
  - Columns: `id` (PK), `ticker_id` (FK), `date`, `open`, `high`, `low`, `close`, `volume`,
    `sma_50`, `sma_200`, `52_week_high`, `percent_from_high`, `book_value_per_share`, `price_to_book`, `enterprise_value`.

- **signal_events**
  - Stores detected trading signals.
  - Columns: `id` (PK), `ticker_id` (FK), `date`, `signal_type` (`golden_cross` or `death_cross`).

**Notes:**
- Unique constraints are applied to prevent duplicate entries.
- Idempotent inserts (`INSERT OR REPLACE`) ensure the pipeline can be re-run safely.

---

## 5. Design Decisions

Key design considerations implemented in the pipeline:

- **Forward-fill fundamentals**
  - Fundamental data (quarterly/annual) is forward-filled to match daily prices, ensuring proper metric calculation for days without fresh reports.

- **Handling missing or partial data**
  - This ensures that even for recent IPOs or incomplete datasets, the pipeline can produce results.

  - Database insert operations are idempotent (`INSERT OR REPLACE`) to avoid duplicates and allow safe re-runs.

- **Cross-market ticker handling**
  - Supports both US and Indian stocks.
  - Ticker formats like `AAPL` (US) or `RELIANCE.NS` (India) are automatically handled.

  * **Cross-market tickers**: US (`AAPL`), India (`RELIANCE.NS`) both supported.
* **Error handling**:

  * Logging (no prints)
  * API failures handled gracefully
  * Partial data processed where possible

---

## 6. Data Quality Notes


  - For tickers with <200 trading days, metrics like 200-day SMA are skipped or calculated partially.
  
  - All incoming data is validated using Pydantic schemas.
  - Invalid or missing data points are logged and skipped without breaking the pipeline.

  - Detailed logs are maintained for data fetches, fallbacks, and metric calculations.
  - Helps identify anomalies, missing data, or API failures.
  
  - Designed to produce outputs even when some data is missing.
  - JSON summaries include metadata indicating the source of fundamental data used (`quarterly`, `annual`, or `info`).


## 📊 Example Output

```json
{
   "ticker": "SWIGGY.NS",
  "generated_at": "2025-10-01T22:23:00.782326",
  "price_rows_count": 221,
  "fundamentals_used": "quarterly_balance_sheet",
  "signals": [
    {
      "date": "2025-01-27T00:00:00",
      "signal_type": "golden_cross",
      "meta": {}
    }
]
}
```
Tests cover:

* SMA & ratio calculations
* Golden/Death cross detection
* Validation with Pydantic

---
---
