import json
import os
from datetime import date
from pathlib import Path
from typing import Optional
import typer
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import Base
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
def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    typer.echo("🔧 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ Base de datos inicializada")

@app.command()
def fetch(output: Optional[Path] = typer.Option(None, help="Ruta del JSON descargado")):
    """Descarga los datos de la API del Ministerio"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    typer.echo("📡 Descargando datos de la API...")
    try:
        payload = fetch_estaciones()
        fn = output or (RAW_DIR / f"{date.today().isoformat()}.json")
        fn.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"✅ Descargado: {fn}")
    except Exception as e:
        typer.echo(f"❌ Error al descargar: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def load(input_file: Optional[Path] = typer.Option(None, help="JSON a cargar; por defecto el de hoy")):
    """Carga los datos en la base de datos"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    if input_file is None:
        input_file = RAW_DIR / f"{date.today().isoformat()}.json"
    
    if not input_file.exists():
        typer.echo(f"❌ No existe {input_file}. Ejecuta primero: python -m app.cli fetch", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"📂 Cargando datos desde {input_file}...")
    
    try:
        payload = json.loads(input_file.read_text(encoding="utf-8"))
        stations, prices = normalize(payload)
        
        db = get_db()
        try:
            n_st = upsert_stations(db, stations)
            n_pr = insert_prices_snapshot(db, prices)
            db.commit()
            typer.echo(f"✅ Estaciones actualizadas: {n_st}")
            typer.echo(f"✅ Precios insertados: {n_pr}")
        finally:
            db.close()
            
    except Exception as e:
        typer.echo(f"❌ Error al cargar datos: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def etl():
    """Ejecuta el proceso ETL completo (fetch + load)"""
    typer.echo("🚀 Ejecutando ETL completo...")
    fetch()
    load()
    validate()

@app.command()
def validate(fecha: Optional[str] = typer.Option(None, help="Fecha YYYY-MM-DD; por defecto hoy")):
    """Valida los datos cargados"""
    from sqlalchemy import text
    
    d = fecha or date.today().isoformat()
    db = get_db()
    
    try:
        # Validar estaciones
        stations_count = db.execute(text("SELECT COUNT(*) FROM stations")).scalar()
        
        # Validar precios
        query = text("""
        SELECT 
            COUNT(*) AS total,
            COUNT(DISTINCT station_id) as stations_with_prices,
            COUNT(DISTINCT fuel_type) as fuel_types,
            SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS nulls,
            MIN(price) AS min_price,
            MAX(price) AS max_price,
            AVG(price) AS avg_price
        FROM prices_daily 
        WHERE date = :d
        """)
        
        row = db.execute(query, {"d": d}).mappings().first()
        
        typer.echo(f"\n📊 Validación para {d}:")
        typer.echo(f"  • Estaciones totales: {stations_count}")
        typer.echo(f"  • Registros de precios: {row['total']}")
        typer.echo(f"  • Estaciones con precios: {row['stations_with_prices']}")
        typer.echo(f"  • Tipos de combustible: {row['fuel_types']}")
        typer.echo(f"  • Precios nulos: {row['nulls']}")
        typer.echo(f"  • Precio mínimo: {row['min_price']:.3f}€" if row['min_price'] else "  • Precio mínimo: N/A")
        typer.echo(f"  • Precio máximo: {row['max_price']:.3f}€" if row['max_price'] else "  • Precio máximo: N/A")
        typer.echo(f"  • Precio promedio: {row['avg_price']:.3f}€" if row['avg_price'] else "  • Precio promedio: N/A")
        
        # Validación de rangos
        if row['min_price'] and row['max_price']:
            ok_range = 0.5 <= row['min_price'] <= 3.0 and row['max_price'] <= 5.0
            typer.echo(f"  • Rango de precios válido: {'✅ Sí' if ok_range else '⚠️  No'}")
        
    finally:
        db.close()

if __name__ == "__main__":
    app()