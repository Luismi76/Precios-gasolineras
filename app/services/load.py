from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text
from app.models import Station, PriceDaily

def upsert_stations(db: Session, stations: List[Dict[str, Any]]) -> int:
    """
    Inserta o actualiza estaciones usando INSERT...ON CONFLICT
    """
    if not stations:
        return 0
    
    # Usar insert de SQLAlchemy con ON CONFLICT
    stmt = insert(Station).values(stations)
    
    # Actualizar todas las columnas excepto la clave primaria
    update_columns = {
        col.name: col 
        for col in stmt.excluded 
        if col.name != "ideess"
    }
    
    stmt = stmt.on_conflict_do_update(
        index_elements=["ideess"],
        set_=update_columns
    )
    
    result = db.execute(stmt)
    db.flush()
    
    return result.rowcount or len(stations)

def insert_prices_snapshot(db: Session, prices: List[Dict[str, Any]]) -> int:
    """
    Inserta precios del día, ignorando duplicados
    """
    if not prices:
        return 0
    
    # Usar INSERT...ON CONFLICT DO NOTHING
    stmt = insert(PriceDaily).values(prices)
    stmt = stmt.on_conflict_do_nothing(
        constraint="uq_price_snapshot"
    )
    
    result = db.execute(stmt)
    db.flush()
    
    return result.rowcount or 0

def cleanup_old_prices(db: Session, days_to_keep: int = 30) -> int:
    """
    Elimina precios más antiguos que los días especificados
    """
    query = text("""
        DELETE FROM prices_daily
        WHERE date < CURRENT_DATE - INTERVAL :days DAY
    """)
    
    result = db.execute(query, {"days": days_to_keep})
    db.flush()
    
    return result.rowcount or 0
