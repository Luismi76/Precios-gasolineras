from typing import Literal, Optional
from fastapi import APIRouter, Depends, Query
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
    Busca estaciones y su precio actual (fecha = hoy) filtrando por fuel_type/provincia.
    """
    query = """
        SELECT
          s.ideess, s.rotulo, s.direccion, s.localidad, s.provincia,
          p.fuel_type, p.price, p.date
        FROM stations s
        JOIN prices_daily p ON p.station_id = s.ideess
        WHERE 1=1
          AND p.date = CURRENT_DATE
    """
    params: dict[str, object] = {}
    if fuel_type:
        query += " AND p.fuel_type = :fuel_type"
        params["fuel_type"] = fuel_type.upper()
    if provincia:
        query += " AND s.provincia ILIKE :provincia"
        params["provincia"] = f"%{provincia}%"

    order = "p.price ASC, s.rotulo ASC" if orden == "precio" else "s.rotulo ASC, p.price ASC"
    query += f" ORDER BY {order} LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    rows = db.execute(text(query), params).mappings().all()
    return {"total": len(rows), "items": [dict(r) for r in rows]}
