-- Catálogos
CREATE TABLE IF NOT EXISTS ref_ccaa (
  id_ccaa TEXT PRIMARY KEY,
  nombre  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ref_provincia (
  id_prov TEXT PRIMARY KEY,
  nombre  TEXT NOT NULL,
  id_ccaa TEXT NOT NULL REFERENCES ref_ccaa(id_ccaa)
);

CREATE TABLE IF NOT EXISTS ref_municipio (
  id_mun  TEXT PRIMARY KEY,
  nombre  TEXT NOT NULL,
  id_prov TEXT NOT NULL REFERENCES ref_provincia(id_prov)
);

CREATE TABLE IF NOT EXISTS ref_producto (
  id_producto TEXT PRIMARY KEY,
  nombre      TEXT NOT NULL
);

-- Estaciones
CREATE TABLE IF NOT EXISTS estaciones (
  ideess     TEXT PRIMARY KEY,
  rotulo     TEXT,
  direccion  TEXT,
  localidad  TEXT,
  provincia  TEXT,
  cp         TEXT,
  latitud    DOUBLE PRECISION,
  longitud   DOUBLE PRECISION
);

-- Precios
CREATE TABLE IF NOT EXISTS precios (
  fecha       DATE NOT NULL,
  ideess      TEXT NOT NULL REFERENCES estaciones(ideess),
  id_producto TEXT NOT NULL REFERENCES ref_producto(id_producto),
  precio      NUMERIC(10,3),
  PRIMARY KEY (fecha, ideess, id_producto)
);

CREATE INDEX IF NOT EXISTS idx_precios_producto ON precios(id_producto);
CREATE INDEX IF NOT EXISTS idx_precios_fecha ON precios(fecha);
