from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base
from app.routers import health, search, stations, ranking, history, lists

# Crear tablas si no existen (para dev; en prod usa migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Precio Gasolineras",
    description="API REST para consultar precios de combustibles en España",
    version="1.0.0",
)

# CORS abierto por defecto; restringe dominios en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(search.router)
app.include_router(stations.router)
app.include_router(ranking.router)
app.include_router(history.router)
app.include_router(lists.router)

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
            "provinces": "/api/provinces",
        },
    }
