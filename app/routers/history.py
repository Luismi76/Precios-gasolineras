from fastapi import APIRouter, Depends, HTTPException, Query
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
    db: Session = Depends(get_db)
):
    """Histórico de precios de una estación para un producto"""
    try:
        query = """
        SELECT date, price
        FROM prices_daily
        WHERE station_id = :ideess AND fuel_type = :fuel_type
        """
        
        params = {"ideess": ideess, "fuel_type": fuel_type.upper()}
        
        if desde:
            query += " AND date >= :desde"
            params["desde"] = desde
        
        if hasta:
            query += " AND date <= :hasta"
            params["hasta"] = hasta
        
        query += " ORDER BY date"
        
        result = db.execute(text(query), params)
        rows = result.mappings().all()
        
        return {
            "station_id": ideess,
            "fuel_type": fuel_type,
            "series": [{"date": str(row["date"]), "price": float(row["price"]) if row["price"] else None} 
                      for row in rows]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
