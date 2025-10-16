from fastapi import FastAPI
from app.routers import health, search  # ⬅️ añade search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Precio Gasolineras")

# /healthz
app.include_router(health.router, prefix="", tags=["health"])

# /api/search
app.include_router(search.router)  # ⬅️ tu router ya trae prefix="/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # para pruebas; luego restringe a tu IP/host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
