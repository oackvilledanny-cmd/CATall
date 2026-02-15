# CA Tall: Canadian Volatility Scanner (TSX/TSXV-ready)

> **Not financial advice.** This project is for informational and educational purposes only.

## 1) Architecture (Google Cloud + Firebase)
- **Frontend:** Next.js (`/frontend`) deploy to Firebase Hosting.
- **Auth:** Firebase Authentication (Email/Google) integration point in Login page.
- **Backend:** FastAPI (`/backend`) deploy to Cloud Run.
- **DB/Cache:** Firestore for user profile, watchlist, cached backtests (MVP save-point prepared).
- **Scheduler:** Cloud Scheduler -> call `/api/scan` for refresh jobs.
- **Secrets:** Use Secret Manager / runtime env vars (`APP_*`), never hardcode API keys.

## 2) MVP features implemented
- Volatility scanner: last N days, count of `|daily return| >= threshold`.
- Technical indicators: EMA20/50, RSI14, MACD(12,26,9), Bollinger(20,2), ATR14, ADX14.
- Bullish scoring (0~100) with reason strings.
- Symbol detail APIs for chart bars, indicators, and news summary (mock provider).
- Portfolio weights API with risk profile constraints and ATR-based TP/SL examples.
- Backtest API with CAGR, max drawdown, win rate, avg trade return, trades, equity curve.
- Every page/API includes **Not financial advice** disclaimer.

## 3) Repository structure
- `frontend/` Next.js UI (Login / Scanner / Symbol detail / Portfolio / Backtest)
- `backend/` FastAPI API and strategy logic
- `infra/` deployment script for Cloud Run + Firebase Hosting

## 4) Backend API endpoints
- `GET /api/scan?days=60&threshold=0.10`
- `GET /api/symbol/{ticker}/chart`
- `GET /api/symbol/{ticker}/indicators`
- `GET /api/symbol/{ticker}/news`
- `POST /api/portfolio/weights`
- `POST /api/backtest`

## 5) Local run
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

## 6) Deploy (one script)
Prereqs: `gcloud auth login`, `gcloud config set project <PROJECT_ID>`, `firebase login`.

```bash
PROJECT_ID=<your-project> REGION=northamerica-northeast1 ./infra/deploy.sh
```

This deploys backend to Cloud Run and frontend to Firebase Hosting.

## 7) Risk-profile guardrails
`POST /api/portfolio/weights` input requires:
- `level`: conservative/balanced/aggressive
- `max_positions`
- `max_weight_per_asset`
- `max_drawdown_limit`

The API truncates ticker list to `max_positions`, caps weights by `max_weight_per_asset`, and returns explanatory notes.

## 8) Provider abstraction
- Price provider interface implemented with `YFinancePriceProvider`.
- News provider interface implemented with `MockNewsProvider` (replace with NewsAPI/Finnhub/GDELT etc).
- Keep API keys in Secret Manager / env vars.

## 9) Testing
```bash
cd backend
PYTHONPATH=. pytest -q
```
Includes:
- indicator unit tests
- scoring unit tests
- e2e-ish API flow test with fake provider

## 10) Demo tickers
Default TSX symbols file: `backend/app/core/tsx_symbols.txt`.
Suggested quick demo: `SHOP.TO`, `ENB.TO`, `SU.TO`.
