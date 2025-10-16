from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/api", tags=["lists"])

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    """Lista de productos/combustibles disponibles"""
    try:
        query = """
        SELECT DISTINCT fuel_type as id_producto, fuel_type as nombre
        FROM prices_daily
        ORDER BY fuel_type
        """
        result = db.execute(text(query))
        rows = result.mappings().all()
        
        fuel_names = {
            "G95_E5": "Gasolina 95 E5",
            "G98_E5": "Gasolina 98 E5",
            "GOA": "Gasóleo A",
            "GOA_PLUS": "Gasóleo Premium",
            "GLP": "Gas Licuado del Petróleo",
            "GNC": "Gas Natural Comprimido",
            "GNL": "Gas Natural Licuado",
            "G95_E10": "Gasolina 95 E10",
            "G98_E10": "Gasolina 98 E10"
        }
        
        products = []
        for row in rows:
            fuel_type = row["id_producto"]
            products.append({
                "id_producto": fuel_type,
                "nombre": fuel_names.get(fuel_type, fuel_type)
            })
        
        return {"items": products}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/provinces")
def get_provinces(db: Session = Depends(get_db)):
    """Lista de provincias con estaciones"""
    try:
        query = """
        SELECT DISTINCT provincia as nombre
        FROM stations
        WHERE provincia IS NOT NULL
        ORDER BY provincia
        """
        result = db.execute(text(query))
        rows = result.mappings().all()
        
        return {"items": [dict(row) for row in rows]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
