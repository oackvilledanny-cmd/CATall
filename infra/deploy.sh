#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID=${PROJECT_ID:?set PROJECT_ID}
REGION=${REGION:-northamerica-northeast1}
BACKEND_SERVICE=${BACKEND_SERVICE:-catall-api}

# Build and deploy backend to Cloud Run
gcloud builds submit ./backend --tag gcr.io/${PROJECT_ID}/${BACKEND_SERVICE}
gcloud run deploy ${BACKEND_SERVICE} \
  --image gcr.io/${PROJECT_ID}/${BACKEND_SERVICE} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars APP_DEFAULT_SYMBOLS_FILE=/app/app/core/tsx_symbols.txt

API_URL=$(gcloud run services describe ${BACKEND_SERVICE} --region ${REGION} --format='value(status.url)')

# Firebase hosting for frontend (expects firebase init done)
(cd frontend && npm ci && NEXT_PUBLIC_API_BASE=${API_URL} npm run build)
firebase deploy --only hosting

echo "Deployed API: ${API_URL}"
