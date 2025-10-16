from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint, Index, Numeric
from datetime import datetime, date
from app.db import Base

class Station(Base):
    __tablename__ = "stations"
    
    ideess: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rotulo: Mapped[str | None] = mapped_column(String(120))
    direccion: Mapped[str | None] = mapped_column(String(240))
    localidad: Mapped[str | None] = mapped_column(String(120))
    provincia: Mapped[str | None] = mapped_column(String(120), index=True)
    ccaa: Mapped[str | None] = mapped_column(String(120), index=True)
    cp: Mapped[str | None] = mapped_column(String(10))
    lat: Mapped[float | None] = mapped_column(Float)
    lon: Mapped[float | None] = mapped_column(Float)
    
    prices: Mapped[list["PriceDaily"]] = relationship(back_populates="station", cascade="all, delete-orphan")

class PriceDaily(Base):
    __tablename__ = "prices_daily"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("stations.ideess", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date, index=True)
    fuel_type: Mapped[str] = mapped_column(String(50))
    price: Mapped[float | None] = mapped_column(Numeric(10, 3))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    station: Mapped[Station] = relationship(back_populates="prices")
    
    __table_args__ = (
        UniqueConstraint("station_id", "date", "fuel_type", name="uq_price_snapshot"),
        Index("ix_price_fuel_date", "fuel_type", "date"),
        Index("ix_price_station_date", "station_id", "date"),
    )