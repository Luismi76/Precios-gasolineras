from typing import Iterable, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models import Station, PriceDaily

def upsert_stations(db: Session, stations: Iterable[Dict[str, Any]]) -> int:
    stations = list(stations)
    if not stations: return 0
    stmt = insert(Station).values(stations)
    update_cols = {c.name: c for c in Station.__table__.c if c.name != "ideess"}
    res = db.execute(stmt.on_conflict_do_update(index_elements=[Station.ideess], set_=update_cols))
    return res.rowcount or 0

def insert_prices_snapshot(db: Session, prices: Iterable[Dict[str, Any]]) -> int:
    prices = list(prices)
    if not prices: return 0
    stmt = insert(PriceDaily).values(prices)
    res = db.execute(stmt.on_conflict_do_nothing(constraint="uq_price_snapshot"))
    return res.rowcount or 0
