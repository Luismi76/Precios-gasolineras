from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/api", tags=["estaciones"])

@router.get("/estacion/{ideess}")
def estacion(ideess: str, db: Session = Depends(get_db)):
    e = db.execute("SELECT * FROM estaciones WHERE ideess=:id", {"id": ideess}).mappings().first()
    if not e: return {"detail": "Not found"}
    precios = db.execute("SELECT id_producto, precio, fecha FROM vw_precio_actual WHERE ideess=:id",
                         {"id": ideess}).mappings().all()
    return {"estacion": e, "precios": precios}
