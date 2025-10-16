from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/api", tags=["lists"])

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    query = """
      SELECT DISTINCT fuel_type AS id_producto, fuel_type AS nombre
      FROM prices_daily ORDER BY fuel_type
    """
    rows = db.execute(text(query)).mappings().all()
    fuel_names = {
        "G95_E5": "Gasolina 95 E5",
        "G98_E5": "Gasolina 98 E5",
        "GOA": "Gasóleo A",
        "GOA_PLUS": "Gasóleo A+",
        "GLP": "GLP",
        "GNC": "GNC",
        "GNL": "GNL",
        "G95_E10": "Gasolina 95 E10",
        "G98_E10": "Gasolina 98 E10",
    }
    return [{"id": r["id_producto"], "nombre": fuel_names.get(r["id_producto"], r["id_producto"])} for r in rows]

@router.get("/provinces")
def get_provinces(db: Session = Depends(get_db)):
    query = "SELECT DISTINCT provincia FROM stations WHERE provincia IS NOT NULL ORDER BY provincia"
    rows = db.execute(text(query)).scalars().all()
    return rows
