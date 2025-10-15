from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, Numeric, Float, ForeignKey

class Base(DeclarativeBase):
    pass

class RefCCAA(Base):
    __tablename__ = "ref_ccaa"
    id_ccaa: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)

class RefProvincia(Base):
    __tablename__ = "ref_provincia"
    id_prov: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    id_ccaa: Mapped[str] = mapped_column(String, ForeignKey("ref_ccaa.id_ccaa"))

class RefMunicipio(Base):
    __tablename__ = "ref_municipio"
    id_mun: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    id_prov: Mapped[str] = mapped_column(String, ForeignKey("ref_provincia.id_prov"))

class RefProducto(Base):
    __tablename__ = "ref_producto"
    id_producto: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)

class Estacion(Base):
    __tablename__ = "estaciones"
    ideess: Mapped[str] = mapped_column(String, primary_key=True)
    rotulo: Mapped[str | None] = mapped_column(String)
    direccion: Mapped[str | None] = mapped_column(String)
    localidad: Mapped[str | None] = mapped_column(String)
    provincia: Mapped[str | None] = mapped_column(String)
    cp: Mapped[str | None] = mapped_column(String)
    latitud: Mapped[float | None] = mapped_column(Float)
    longitud: Mapped[float | None] = mapped_column(Float)

class Precio(Base):
    __tablename__ = "precios"
    fecha: Mapped[str] = mapped_column(Date, primary_key=True)
    ideess: Mapped[str] = mapped_column(String, ForeignKey("estaciones.ideess"), primary_key=True)
    id_producto: Mapped[str] = mapped_column(String, ForeignKey("ref_producto.id_producto"), primary_key=True)
    precio: Mapped[float | None] = mapped_column(Numeric(10,3))
