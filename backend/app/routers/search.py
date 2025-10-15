from sqlalchemy import text
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/api", tags=["search"])

@router.get("/search")
def search(
    producto: str | None = None,
    ccaa: str | None = None,
    provincia: str | None = None,
    municipio: str | None = None,
    orden: str | None = "precio",
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = """
      SELECT e.ideess, e.rotulo, e.direccion, e.localidad, e.provincia,
             p.precio
      FROM estaciones e
      JOIN vw_precio_actual p ON p.ideess = e.ideess
      JOIN ref_provincia rp ON rp.nombre = e.provincia
      WHERE 1=1
    """
    params: dict[str, object] = {}

    if producto:
        q += " AND p.id_producto = :prod"
        params["prod"] = producto

    if provincia:
        # Si pasan código (p.ej. "11") filtra por rp.id_prov; si pasan nombre, por e.provincia
        if provincia.isdigit() or len(provincia) <= 3:
            q += " AND rp.id_prov = :prov"
        else:
            q += " AND e.provincia = :prov"
        params["prov"] = provincia

    if orden == "precio":
        q += " ORDER BY p.precio ASC NULLS LAST"
    else:
        q += " ORDER BY e.rotulo"

    q += " LIMIT :lim OFFSET :off"
    params.update({"lim": limit, "off": offset})

    rows = db.execute(text(q), params).mappings().all()
    return {"items": rows, "count": len(rows)}
