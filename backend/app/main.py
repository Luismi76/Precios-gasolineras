from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import lists, search, stations, ranking, history

app = FastAPI(title="PrecioGasolineras API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lists.router)
app.include_router(search.router)
app.include_router(stations.router)
app.include_router(ranking.router)
app.include_router(history.router)

@app.get("/health")
def health():
    return {"ok": True}
