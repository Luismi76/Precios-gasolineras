# app/routers/search.py
from typing import Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db import get_db

router = APIRouter(prefix="/api", tags=["search"])

@router.get("/search")
def search(
    fuel_type: str | None = Query(None, description="Ej.: G95, GOA, GLP…"),
    provincia: str | None = Query(None, description="Nombre o parte, ej.: Sevilla"),
    orden: Literal["precio", "rotulo"] = Query("precio", description="Orden: precio|rotulo"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Snapshot del día (p.date = CURRENT_DATE) uniendo stations + prices_daily.
    Columnas: stations(ideess, rotulo, direccion, localidad, provincia, lat, lon)
              prices_daily(station_id, date, fuel_type, price)
    """

    q = """
    SELECT
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
    params: dict[str, object] = {}

    if fuel_type:
        q += " AND p.fuel_type = :fuel_type"
        params["fuel_type"] = fuel_type

    if provincia:
        prov = provincia.strip()
        q += " AND s.provincia ILIKE :provpat"
        params["provpat"] = f"%{prov}%"

    if orden == "rotulo":
        q += " ORDER BY s.rotulo ASC, p.price ASC NULLS LAST"
    else:
        q += " ORDER BY p.price ASC NULLS LAST, s.rotulo ASC"

    q += " LIMIT :lim OFFSET :off"
    params.update({"lim": limit, "off": offset})

    rows = db.execute(text(q), params).mappings().all()
    return {"items": rows, "count": len(rows)}
