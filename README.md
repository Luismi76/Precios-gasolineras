# PrecioGasolineras (MVP)

Monorepo mínimo para API + Web + Postgres.

## Puesta en marcha rápida

```bash
cp .env.example .env
docker compose up -d postgres adminer
# espera 5-10s a que inicie y cree tablas
docker compose up backend -d
docker compose exec backend bash backend/scripts/run_etl.sh
docker compose up frontend -d
```

- Adminer: http://localhost:8080
- API: http://localhost:8000/health
- Web: http://localhost:5173
