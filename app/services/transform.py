from typing import Any, Dict, Iterable, List
from datetime import date
FUEL_KEYS = {
    "Precio Gasolina 95 E5": "G95_E5",
    "Precio Gasolina 98 E5": "G98_E5",
    "Precio Gasoleo A": "GOA",
    "Precio Gasoleo Premium": "GOA_PLUS",
    "Precio GLP": "GLP",
    "Precio GNC": "GNC",
    "Precio GNL": "GNL",
    "Precio Gasolina 95 E10": "G95_E10",
    "Precio Gasolina 98 E10": "G98_E10",
}
def _to_float(s: Any) -> float | None:
    if s is None: return None
    if isinstance(s,(int,float)): return float(s)
    s = str(s).replace(",", ".").strip()
    if not s or s.lower() in ("nan","null"): return None
    try: return float(s)
    except ValueError: return None

def normalize(payload: Dict[str, Any]) -> tuple[list[dict], list[dict]]:
    registros: Iterable[Dict[str, Any]] = payload.get("ListaEESSPrecio", []) or payload.get("EstacionesTerrestres", [])
    d = date.today()
    stations: List[Dict[str, Any]] = []; prices: List[Dict[str, Any]] = []
    for row in registros:
        ideess = int(row.get("IDEESS")) if row.get("IDEESS") else None
        if not ideess: continue
        stations.append({
            "ideess": ideess,
            "rotulo": row.get("Rótulo"),
            "direccion": row.get("Dirección"),
            "localidad": row.get("Localidad"),
            "provincia": row.get("Provincia"),
            "cp": row.get("C.P."),
            "lat": _to_float(row.get("Latitud")),
            "lon": _to_float(row.get("Longitud (WGS84)")),
            "ccaa": row.get("CCAA") or row.get("IDCCAA") or None,
        })
        for k, fuel in FUEL_KEYS.items():
            if k in row:
                prices.append({"station_id": ideess, "date": d, "fuel_type": fuel, "price": _to_float(row.get(k))})
    return stations, prices
