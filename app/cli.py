import json
import os
from datetime import date
from pathlib import Path
from typing import Optional
import pandas as pd
import typer
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.api_client import fetch_estaciones
from app.services.transform import normalize
from app.services.load import upsert_stations, insert_prices_snapshot

app = typer.Typer(add_completion=False, help="CLI ETL Gasolineras")

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
RAW_DIR = DATA_DIR / "raw"
EXPORT_DIR = DATA_DIR / "exports"

def get_db() -> Session:
    return SessionLocal()

@app.command()
def fetch(output: Optional[Path] = typer.Option(None, help="Ruta del JSON descargado")):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    payload = fetch_estaciones()
    fn = output or (RAW_DIR / f"{date.today().isoformat()}.json")
    fn.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    typer.echo(f"✅ Descargado: {fn}")

@app.command()
def load(input_file: Optional[Path] = typer.Option(None, help="JSON a cargar; por defecto el de hoy")):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if input_file is None:
        input_file = RAW_DIR / f"{date.today().isoformat()}.json"
    if not input_file.exists():
        raise typer.BadParameter(f"No existe {input_file}. Ejecuta primero: fetch")
    payload = json.loads(input_file.read_text(encoding="utf-8"))
    stations, prices = normalize(payload)
    db = get_db()
    try:
        n_st = upsert_stations(db, stations)
        n_pr = insert_prices_snapshot(db, prices)
        db.commit()
        typer.echo(f"✅ Upsert estaciones: {n_st} | Insert precios (snapshot): {n_pr}")
    finally:
        db.close()

@app.command()
def validate(fecha: Optional[str] = typer.Option(None, help="Fecha YYYY-MM-DD; por defecto hoy")):
    from sqlalchemy import text
    d = fecha or date.today().isoformat()
    db = get_db()
    try:
        q = text("""
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS nulls,
               MIN(price) AS min_p, MAX(price) AS max_p
        FROM prices_daily WHERE date = :d
        """)
        row = db.execute(q, {"d": d}).mappings().one()
        ok_range = (row["min_p"] or 0) >= 0 and (row["max_p"] or 0) <= 5.0
        typer.echo(f"📊 {d} → total={row['total']} nulls={row['nulls']} min={row['min_p']} max={row['max_p']} rango_ok={ok_range}")
    finally:
        db.close()

if __name__ == "__main__":
    app()
