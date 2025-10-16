from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.db import get_db

router = APIRouter(prefix="/api", tags=["ranking"])

@router.get("/ranking")
def ranking(
    scope: str = Query(..., description="Ámbito: 'nacional' o 'provincia:NombreProvincia'"),
    fuel_type: str = Query(..., description="Tipo de combustible"),
    fecha: Optional[str] = Query(None, description="Fecha YYYY-MM-DD (por defecto hoy)"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Ranking de estaciones más baratas por ámbito y producto"""
    try:
        query = """
        SELECT 
            s.ideess,
            s.rotulo,
            s.localidad,
            s.provincia,
            p.price
        FROM prices_daily p
        JOIN stations s ON s.ideess = p.station_id
        WHERE p.fuel_type = :fuel_type
        """
        
        params = {"fuel_type": fuel_type.upper()}
        
        if fecha:
            query += " AND p.date = :fecha"
            params["fecha"] = fecha
        else:
            query += " AND p.date = CURRENT_DATE"
        
        if scope.startswith("provincia:"):
            provincia = scope.split(":", 1)[1]
            query += " AND s.provincia ILIKE :provincia"
            params["provincia"] = f"%{provincia}%"
        
        query += " AND p.price IS NOT NULL ORDER BY p.price ASC LIMIT :limit"
        params["limit"] = limit
        
        result = db.execute(text(query), params)
        rows = result.mappings().all()
        
        return {
            "scope": scope,
            "fuel_type": fuel_type,
            "date": fecha or "current",
            "items": [dict(row) for row in rows]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))