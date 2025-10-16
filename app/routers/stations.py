from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/api", tags=["stations"])

@router.get("/station/{ideess}")
def get_station(ideess: int, db: Session = Depends(get_db)):
    """Obtiene información detallada de una estación"""
    try:
        # Información de la estación
        station_query = """
        SELECT ideess, rotulo, direccion, localidad, provincia, cp, lat, lon
        FROM stations
        WHERE ideess = :ideess
        """
        station = db.execute(text(station_query), {"ideess": ideess}).mappings().first()
        
        if not station:
            raise HTTPException(status_code=404, detail="Estación no encontrada")
        
        # Precios actuales
        prices_query = """
        SELECT fuel_type, price, date
        FROM prices_daily
        WHERE station_id = :ideess AND date = CURRENT_DATE
        ORDER BY fuel_type
        """
        prices = db.execute(text(prices_query), {"ideess": ideess}).mappings().all()
        
        return {
            "station": dict(station),
            "current_prices": [dict(p) for p in prices]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))