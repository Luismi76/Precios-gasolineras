import time
from typing import Any, Dict
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def _create_session() -> requests.Session:
    """Crea una sesión con reintentos robustos"""
    session = requests.Session()
    
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    session.headers.update({
        "User-Agent": "PrecioGasolineras/1.0",
        "Accept": "application/json",
        "Connection": "close",
    })
    
    return session

def fetch_estaciones(max_retries: int = 3, base_delay: float = 2.0) -> Dict[str, Any]:
    """Descarga los datos de estaciones desde la API del Ministerio"""
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    
    session = _create_session()
    last_error = None
    
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            # Validar que tenemos datos
            if "ListaEESSPrecio" in data and data["ListaEESSPrecio"]:
                return data
            elif "EstacionesTerrestres" in data:
                return data
            else:
                raise ValueError("Respuesta sin datos de estaciones")
                
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = base_delay * (2 ** attempt)
                time.sleep(wait_time)
    
    raise RuntimeError(f"Error tras {max_retries} intentos: {last_error}")
