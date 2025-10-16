from fastapi import APIRouter, Depends, Query
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
    db: Session = Depends(get_db),
):
    query = """
      SELECT s.ideess, s.rotulo, s.localidad, s.provincia, p.price, p.date
      FROM stations s
      JOIN prices_daily p ON p.station_id = s.ideess
      WHERE p.fuel_type = :fuel_type
    """
    params: dict[str, object] = {"fuel_type": fuel_type.upper()}
    if fecha:
        query += " AND p.date = :fecha"
        params["fecha"] = fecha
    else:
        query += " AND p.date = CURRENT_DATE"

    if scope.startswith("provincia:"):
        provincia = scope.split(":", 1)[1]
        query += " AND s.provincia ILIKE :provincia"
        params["provincia"] = f"%{provincia}%"

    query += " ORDER BY p.price ASC, s.rotulo ASC LIMIT :limit"
    params["limit"] = limit

    rows = db.execute(text(query), params).mappings().all()
    return {"items": [dict(r) for r in rows]}
