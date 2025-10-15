#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=/app
python - <<'PY'
from datetime import date
from app.db import SessionLocal
from app.services.energia_client import EnergiaClient
from app.services.etl import upsert_estaciones, upsert_precios_diarios

cli = EnergiaClient()
with SessionLocal() as db:
    rows = cli.estaciones()
    upsert_estaciones(db, rows)
    # MVP: Gasóleo A (id 4) leyendo el campo JSON "Precio Gasóleo A"
    upsert_precios_diarios(db, date.today(), rows, "4", "Precio Gasóleo A")
print("ETL OK")
PY
