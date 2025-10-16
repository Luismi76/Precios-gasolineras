from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint, Index
from datetime import datetime
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
    prices: Mapped[list["PriceDaily"]] = relationship(back_populates="station")

class PriceDaily(Base):
    __tablename__ = "prices_daily"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("stations.ideess", ondelete="CASCADE"))
    date: Mapped[datetime] = mapped_column(Date, index=True)
    fuel_type: Mapped[str] = mapped_column(String(50))
    price: Mapped[float | None] = mapped_column(Float)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    station: Mapped[Station] = relationship(back_populates="prices")
    __table_args__ = (
        UniqueConstraint("station_id", "date", "fuel_type", name="uq_price_snapshot"),
        Index("ix_price_fuel_prov", "fuel_type", "date"),
    )
