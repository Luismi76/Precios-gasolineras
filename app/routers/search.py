# ============== app/routers/search.py ==============
from typing import Literal, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/api", tags=["search"])

@router.get("/search")
def search(
    fuel_type: Optional[str] = Query(None, description="Tipo de combustible: G95_E5, GOA, GLP..."),
    provincia: Optional[str] = Query(None, description="Nombre o parte de la provincia"),
    orden: Literal["precio", "rotulo"] = Query("precio", description="Ordenar por precio o nombre"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Busca estaciones con filtros opcionales.
    Devuelve el snapshot del día actual.
    """
    try:
        query = """
        SELECT DISTINCT
            s.ideess,
            s.rotulo,
            s.direccion,
            s.localidad,
            s.provincia,
            s.lat,
            s.lon,
            p.fuel_type,
            p.price,
            p.date
        FROM stations s
        JOIN prices_daily p ON p.station_id = s.ideess
        WHERE p.date = CURRENT_DATE
        """
        
        params = {}
        
        if fuel_type:
            query += " AND p.fuel_type = :fuel_type"
            params["fuel_type"] = fuel_type.upper()
        
        if provincia:
            query += " AND s.provincia ILIKE :provincia"
            params["provincia"] = f"%{provincia}%"
        
        # Ordenamiento
        if orden == "rotulo":
            query += " ORDER BY s.rotulo ASC, p.price ASC NULLS LAST"
        else:
            query += " ORDER BY p.price ASC NULLS LAST, s.rotulo ASC"
        
        query += " LIMIT :limit OFFSET :offset"
        params["limit"] = limit
        params["offset"] = offset
        
        result = db.execute(text(query), params)
        rows = result.mappings().all()
        
        return {
            "items": [dict(row) for row in rows],
            "count": len(rows),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))