from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.db import get_db

router = APIRouter(prefix="/api", tags=["history"])

@router.get("/history/station/{ideess}")
def station_history(
    ideess: int,
    fuel_type: str = Query(..., description="Tipo de combustible"),
    desde: Optional[str] = Query(None, description="Fecha desde YYYY-MM-DD"),
    hasta: Optional[str] = Query(None, description="Fecha hasta YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = """
      SELECT date, price
      FROM prices_daily
      WHERE station_id = :ideess AND fuel_type = :fuel_type
    """
    params: dict[str, object] = {"ideess": ideess, "fuel_type": fuel_type.upper()}
    if desde:
        query += " AND date >= :desde"
        params["desde"] = desde
    if hasta:
        query += " AND date <= :hasta"
        params["hasta"] = hasta
    query += " ORDER BY date"

    rows = db.execute(text(query), params).mappings().all()
    return {
        "station_id": ideess,
        "fuel_type": fuel_type.upper(),
        "series": [{"date": str(r["date"]), "price": float(r["price"]) if r["price"] is not None else None} for r in rows],
    }
