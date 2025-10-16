# Precios-gasolineras — ETL + API de precios

[![CI](https://img.shields.io/github/actions/workflow/status/Luismi76/Precios-gasolineras/ci.yml?label=CI)](../../actions)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Style](https://img.shields.io/badge/style-black%2Bruff-black)

API y pipeline para consultar precios de carburantes en estaciones de servicio en España, con
almacenamiento en Postgres y despliegue vía Docker Compose.

## Requisitos
- Docker + Docker Compose
- (Opcional) Python 3.11 para desarrollo local

## Variables de entorno
Crea tu `.env` a partir de `.env.example`. Variables principales:
```env
APP_PORT=8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=gasolineras
POSTGRES_HOST=db
POSTGRES_PORT=5432
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

exit
