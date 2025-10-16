from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, search, stations, ranking, history, lists
from app.db import engine
from app.models import Base

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Precio Gasolineras",
    description="API REST para consultar precios de combustibles en España",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, tags=["Health"])
app.include_router(search.router, tags=["Búsqueda"])
app.include_router(stations.router, tags=["Estaciones"])
app.include_router(ranking.router, tags=["Ranking"])
app.include_router(history.router, tags=["Histórico"])
app.include_router(lists.router, tags=["Listas"])

@app.get("/")
def root():
    return {
        "message": "API Precio Gasolineras",
        "docs": "/docs",
        "endpoints": {
            "health": "/healthz",
            "search": "/api/search",
            "station": "/api/station/{ideess}",
            "ranking": "/api/ranking",
            "history": "/api/history/station/{ideess}",
            "products": "/api/products",
            "provinces": "/api/provinces"
        }
    }