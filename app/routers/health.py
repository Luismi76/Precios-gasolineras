from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter()

@router.get("/healthz")
def healthz():
    """Health check básico"""
    return {"status": "ok"}

@router.get("/health/detailed")
def health_detailed(db: Session = Depends(get_db)):
    """Health check detallado con estado de la BD"""
    try:
        # Verificar conexión a BD
        db.execute(text("SELECT 1"))
        
        # Contar registros
        stations = db.execute(text("SELECT COUNT(*) FROM stations")).scalar()
        prices = db.execute(text("SELECT COUNT(*) FROM prices_daily WHERE date = CURRENT_DATE")).scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "stations_count": stations,
            "today_prices_count": prices
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }