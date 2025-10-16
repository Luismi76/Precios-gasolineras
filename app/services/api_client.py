import time
from typing import Any, Dict
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from app.core.config import get_settings

settings = get_settings()

def _session() -> requests.Session:
    s = requests.Session()
    # Retries robustos (GET) + backoff exponencial
    retry = Retry(
        total=6,
        connect=6,
        read=6,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    s.headers.update({
        "User-Agent": "PrecioGasolineras/1.0 (+https://github.com/Luismi76/Precios-gasolineras)",
        "Accept": "application/json",
        "Connection": "close",
    })
    return s

def fetch_estaciones(max_retries: int = 5, base_delay: float = 1.0) -> Dict[str, Any]:
    url = settings.GAS_API_URL
    last_err = None
    sess = _session()
    for attempt in range(max_retries):
        try:
            r = sess.get(url, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            time.sleep(base_delay * (2 ** attempt))
    raise RuntimeError(f"Fallo al descargar datos tras {max_retries} intentos: {last_err}")
