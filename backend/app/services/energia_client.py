import time, requests
from typing import Any, Dict, Optional

DEFAULT_BASE = "https://energia.serviciosmin.gob.es/ServiciosRestCarburantes/PreciosCarburantes"

class EnergiaClient:
    def __init__(self, base_url: str = DEFAULT_BASE, timeout: int = 40, retries: int = 3, backoff: float = 1.5):
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "PrecioGasolineras/1.0"})

    def _get(self, path: str):
        url = f"{self.base}/{path.lstrip('/')}"
        last_err = None
        for attempt in range(1, self.retries + 1):
            try:
                r = self.s.get(url, timeout=self.timeout)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                last_err = e
                if attempt < self.retries:
                    time.sleep(self.backoff ** attempt)
        raise last_err

    # ===== Helpers para aceptar dict o lista =====
    @staticmethod
    def _unwrap(obj, key):
        # Si viene como dict con la clave esperada, usa esa clave; si es lista, devuélvela tal cual
        if isinstance(obj, dict):
            return obj.get(key, obj)
        return obj

    # ===== Listados =====
    def productos(self):
        return self._unwrap(self._get("Listados/ProductosPetroliferos/"), "ListaProducto")

    def ccaa(self):
        return self._unwrap(self._get("Listados/ComunidadesAutonomas/"), "ListaComunidades")

    def provincias(self):
        return self._unwrap(self._get("Listados/Provincias/"), "ListaProvincias")

    def provincias_por_ccaa(self, id_ccaa: str):
        return self._unwrap(self._get(f"Listados/ProvinciasPorComunidad/{id_ccaa}"), "ListaProvincias")

    def municipios_por_provincia(self, id_prov: str):
        return self._unwrap(self._get(f"Listados/MunicipiosPorProvincia/{id_prov}"), "ListaMunicipios")

    # ===== Estaciones =====
    def estaciones(self):
        return self._unwrap(self._get("EstacionesTerrestres/"), "ListaEESSPrecio")

    def estaciones_provincia_producto(self, id_prov: str, id_producto: str):
        return self._unwrap(self._get(f"EstacionesTerrestres/FiltroProvinciaProducto/{id_prov}/{id_producto}"), "ListaEESSPrecio")

    # ===== Histórico =====
    def hist_provincia_producto(self, fecha: str, id_prov: str, id_producto: str):
        return self._unwrap(self._get(f"EstacionesTerrestresHist/FiltroProvinciaProducto/{fecha}/{id_prov}/{id_producto}"), "ListaEESSPrecio")

def to_float_es(v: Optional[str]) -> Optional[float]:
    if v is None: return None
    try: return float(v.replace(',', '.'))
    except Exception: return None

PRICE_PREFIX = "Precio"

def normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    for k, val in list(out.items()):
        if isinstance(k, str) and k.startswith(PRICE_PREFIX):
            out[k] = to_float_es(val) if isinstance(val, str) else val
    for k in ("Latitud", "Longitud"):
        if k in out: out[k] = to_float_es(out[k])
    return out
