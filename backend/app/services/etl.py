from datetime import date
from typing import Iterable
from sqlalchemy import text
from sqlalchemy.orm import Session
from .energia_client import normalize_row

KEYS_STATION = {
    "IDEESS": "ideess",
    "Rótulo": "rotulo",
    "Dirección": "direccion",
    "Localidad": "localidad",
    "Provincia": "provincia",
    "C.P.": "cp",
    "Latitud": "latitud",
    "Longitud": "longitud",
}

def upsert_estaciones(db: Session, rows: Iterable[dict]):
    sql = text(
        """
        INSERT INTO estaciones (ideess, rotulo, direccion, localidad, provincia, cp, latitud, longitud)
        VALUES (:ideess, :rotulo, :direccion, :localidad, :provincia, :cp, :latitud, :longitud)
        ON CONFLICT (ideess) DO UPDATE SET
          rotulo=EXCLUDED.rotulo,
          direccion=EXCLUDED.direccion,
          localidad=EXCLUDED.localidad,
          provincia=EXCLUDED.provincia,
          cp=EXCLUDED.cp,
          latitud=EXCLUDED.latitud,
          longitud=EXCLUDED.longitud
        """
    )
    for r in rows:
        n = normalize_row(r)
        payload = {dst: n.get(src) for src, dst in KEYS_STATION.items()}
        db.execute(sql, payload)
    db.commit()

def upsert_precios_diarios(db: Session, fecha: date, rows: Iterable[dict], id_producto: str, campo_precio: str):
    sql = text(
        """
        INSERT INTO precios (fecha, ideess, id_producto, precio)
        VALUES (:fecha, :ideess, :id_producto, :precio)
        ON CONFLICT (fecha, ideess, id_producto) DO UPDATE SET precio=EXCLUDED.precio
        """
    )
    for r in rows:
        n = normalize_row(r)
        precio = n.get(campo_precio)
        if precio is None:
            continue
        db.execute(sql, {
            "fecha": fecha,
            "ideess": n.get("IDEESS"),
            "id_producto": id_producto,
            "precio": precio,
        })
    db.commit()
