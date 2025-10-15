from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/api", tags=["historico"])

@router.get("/historico/estacion/{ideess}")
def historico_estacion(ideess: str, producto: str, desde: str | None = None, hasta: str | None = None,
                       db: Session = Depends(get_db)):
    q = "SELECT fecha, precio FROM precios WHERE ideess=:id AND id_producto=:p"
    params = {"id": ideess, "p": producto}
    if desde:
        q += " AND fecha >= :d"; params["d"] = desde
    if hasta:
        q += " AND fecha <= :h"; params["h"] = hasta
    q += " ORDER BY fecha"
    rows = db.execute(q, params).mappings().all()
    return {"series": rows}
