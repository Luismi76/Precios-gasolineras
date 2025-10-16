from typing import Any, Dict, List, Tuple
from datetime import date

# Mapeo de nombres de campo a códigos de combustible
FUEL_MAPPING = {
    "Precio Gasolina 95 E5": "G95_E5",
    "Precio Gasolina 95 E10": "G95_E10",
    "Precio Gasolina 98 E5": "G98_E5",
    "Precio Gasolina 98 E10": "G98_E10",
    "Precio Gasoleo A": "GOA",
    "Precio Gasoleo Premium": "GOA_PLUS",
    "Precio Gasóleo A": "GOA",  # Variante con tilde
    "Precio Gasóleo Premium": "GOA_PLUS",  # Variante con tilde
    "Precio GLP": "GLP",
    "Precio GNC": "GNC",
    "Precio GNL": "GNL",
    "Precio Biodiesel": "BIO",
    "Precio Bioetanol": "BIE",
    "Precio Gases licuados del petróleo": "GLP",
}

def _to_float(value: Any) -> float | None:
    """Convierte un valor a float, manejando formato español"""
    if value is None:
        return None
    
    if isinstance(value, (int, float)):
        return float(value)
    
    # Limpiar y convertir string
    s = str(value).replace(",", ".").strip()
    
    if not s or s.lower() in ("nan", "null", "none", ""):
        return None
    
    try:
        return float(s)
    except ValueError:
        return None

def normalize(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Normaliza los datos de la API del Ministerio.
    Retorna tupla (stations, prices)
    """
    # Obtener lista de registros de diferentes formatos posibles
    registros = (
        payload.get("ListaEESSPrecio", []) or 
        payload.get("EstacionesTerrestres", []) or 
        []
    )
    
    if not registros:
        return [], []
    
    stations = []
    prices = []
    current_date = date.today()
    
    for row in registros:
        # Extraer ID de estación
        ideess_raw = row.get("IDEESS")
        if not ideess_raw:
            continue
            
        try:
            ideess = int(ideess_raw)
        except (ValueError, TypeError):
            continue
        
        # Datos de la estación
        station = {
            "ideess": ideess,
            "rotulo": row.get("Rótulo", "").strip() or None,
            "direccion": row.get("Dirección", "").strip() or None,
            "localidad": row.get("Localidad", "").strip() or None,
            "provincia": row.get("Provincia", "").strip() or None,
            "cp": row.get("C.P.", "").strip() or None,
            "lat": _to_float(row.get("Latitud")),
            "lon": _to_float(row.get("Longitud (WGS84)") or row.get("Longitud")),
            "ccaa": row.get("IDCCAA") or row.get("CCAA") or None,
        }
        stations.append(station)
        
        # Extraer precios de todos los combustibles
        for campo, fuel_code in FUEL_MAPPING.items():
            if campo in row:
                precio = _to_float(row[campo])
                if precio is not None and precio > 0:
                    prices.append({
                        "station_id": ideess,
                        "date": current_date,
                        "fuel_type": fuel_code,
                        "price": precio
                    })
    
    return stations, prices