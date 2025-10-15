from sqlalchemy import text
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/api", tags=["listas"])

@router.get("/productos")
def productos(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id_producto, nombre FROM ref_producto ORDER BY nombre")).mappings().all()
    return {"items": rows}

@router.get("/listas/provincias")
def provincias(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id_prov, nombre FROM ref_provincia ORDER BY nombre")).mappings().all()
    return {"items": rows}

@router.get("/listas/municipios")
def municipios(provincia: str, db: Session = Depends(get_db)):
    rows = db.execute("SELECT id_mun, nombre FROM ref_municipio WHERE id_prov=:p ORDER BY nombre", {"p": provincia}).mappings().all()
    return {"items": rows}
