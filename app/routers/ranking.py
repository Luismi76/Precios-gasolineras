from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/api", tags=["ranking"])

@router.get("/ranking")
def ranking(scope: str, producto: str, fecha: str | None = None, limit: int = 20, db: Session = Depends(get_db)):
    kind, _, value = scope.partition(":")
    base = """
      SELECT e.ideess, e.rotulo, e.localidad, p.precio
      FROM precios p JOIN estaciones e USING(ideess)
      WHERE p.id_producto = :prod
    """
    params = {"prod": producto}
    if fecha:
        base += " AND p.fecha = :f"; params["f"] = fecha
    if kind == "provincia":
        base += " AND e.provincia = :prov"; params["prov"] = value
    base += " ORDER BY p.precio ASC NULLS LAST LIMIT :lim"
    params["lim"] = limit
    rows = db.execute(base, params).mappings().all()
    return {"items": rows}
