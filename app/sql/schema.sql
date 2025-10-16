CREATE TABLE IF NOT EXISTS stations (
  ideess     INTEGER PRIMARY KEY,
  rotulo     TEXT,
  direccion  TEXT,
  localidad  TEXT,
  provincia  TEXT,
  ccaa       TEXT,
  cp         TEXT,
  lat        DOUBLE PRECISION,
  lon        DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS prices_daily (
  id          SERIAL PRIMARY KEY,
  station_id  INTEGER NOT NULL REFERENCES stations(ideess) ON DELETE CASCADE,
  date        DATE NOT NULL,
  fuel_type   TEXT NOT NULL,
  price       NUMERIC(10,3),
  retrieved_at TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_price_snapshot UNIQUE (station_id, date, fuel_type)
);

CREATE INDEX IF NOT EXISTS idx_prices_daily_fuel_date ON prices_daily(fuel_type, date);
CREATE INDEX IF NOT EXISTS idx_prices_daily_station_date ON prices_daily(station_id, date);
