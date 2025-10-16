# app/routers/search.py
from typing import Optional, Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/api", tags=["search"])

# Normaliza entradas típicas a los códigos de tu BD
FUEL_ALIASES = {
    "95": "G95_E5", "g95": "G95_E5", "gasolina95": "G95_E5", "sp95": "G95_E5",
    "95e5": "G95_E5", "g95_e5": "G95_E5", "g95e5": "G95_E5",
    "98": "G98_E5", "g98": "G98_E5", "sp98": "G98_E5",
    "diesel": "GOA", "diésel": "GOA", "gasoleo": "GOA", "gasóleo": "GOA",
    "goa": "GOA", "goa+": "GOA_PLUS", "goa_plus": "GOA_PLUS",
    "glp": "GLP", "gnc": "GNC", "gnl": "GNL", "95e10": "G95_E10", "98e10": "G98_E10",
}

def normalize_fuel(s: Optional[str]) -> Optional[str]:
    if not s: return None
    k = s.strip().lower().replace(" ", "").replace("-", "_")
    return FUEL_ALIASES.get(k, s.strip().upper())

@router.get("/search")
def search(
    fuel_type: Optional[str] = Query(None, description="Ej.: G95, GOA, GLP"),
    provincia: Optional[str] = Query(None, description="Nombre (match parcial, sin distinción de mayúsculas)"),
    orden: Literal["precio", "rotulo"] = Query("precio"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    fuel = normalize_fuel(fuel_type)

    # 1) CTE con la última fecha disponible
    sql = """
    WITH d AS (SELECT max(date) AS latest FROM prices_daily)
    SELECT
      s.ideess, s.rotulo, s.direccion, s.localidad, s.provincia,
      s.lat, s.lon,
      p.fuel_type, p.price, p.date
    FROM stations s
    JOIN prices_daily p
      ON p.station_id = s.ideess
    JOIN d ON p.date = d.latest
    WHERE 1=1
    """
    params = {}

    if fuel:
        sql += " AND p.fuel_type = :fuel"
        params["fuel"] = fuel

    if provincia:
        sql += " AND s.provincia ILIKE :prov"
        params["prov"] = f"%{provincia}%"

    order_sql = "p.price ASC, s.rotulo ASC" if orden == "precio" else "s.rotulo ASC, p.price ASC"
    sql_count = "WITH d AS (SELECT max(date) AS latest FROM prices_daily) SELECT count(*) FROM stations s JOIN prices_daily p ON p.station_id=s.ideess JOIN d ON p.date=d.latest WHERE 1=1"
    if fuel:
        sql_count += " AND p.fuel_type = :fuel"
    if provincia:
        sql_count += " AND s.provincia ILIKE :prov"

    sql += f" ORDER BY {order_sql} LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    total = db.execute(text(sql_count), params).scalar_one()
    rows = db.execute(text(sql), params).mappings().all()

    return {"total": total, "items": [dict(r) for r in rows]}
