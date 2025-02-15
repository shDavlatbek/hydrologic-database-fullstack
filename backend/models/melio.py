from datetime import datetime
from sqlalchemy import Boolean, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.common import NameField
from schemas.geo import GeoWell, Parameter


class Organization(Base):
    __tablename__ = "melio_organization"
    pydantic_model = NameField
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    

class Station(Base):
    __tablename__ = "melio_station"
    pydantic_model = NameField
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)
  

class WellType(Base):
    __tablename__ = "melio_welltype"
    pydantic_model = NameField
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)


class MelioWell(Base):
    __tablename__ = "melio_well"
    pydantic_model = GeoWell
    number: Mapped[int] = mapped_column(nullable=False, unique=True)
    region: Mapped[int] = mapped_column(ForeignKey('region.id'), nullable=True)
    district: Mapped[int] = mapped_column(ForeignKey('district.id'), nullable=True)
    organization: Mapped[int] = mapped_column(ForeignKey('melio_organization.id'), nullable=True)
    station: Mapped[int] = mapped_column(ForeignKey('melio_station.id'), nullable=True)
    location: Mapped[int] = mapped_column(ForeignKey('location.id'), nullable=True)
    well_type: Mapped[int] = mapped_column(ForeignKey('melio_welltype.id'), nullable=True)
    x: Mapped[float] = mapped_column(nullable=True)
    y: Mapped[float] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(String(length=250), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        onupdate=func.now(), 
        default=func.now()
    )
    

class ParameterName(Base):
    __tablename__ = "melio_parametername"
    pydantic_model = NameField
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    

class Parameter(Base):
    __tablename__ = "melio_parameter"
    pydantic_model = Parameter
    well: Mapped[int] = mapped_column(ForeignKey('melio_well.number'), nullable=False)
    parameter_name: Mapped[int] = mapped_column(ForeignKey('melio_parametername.id'), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    value: Mapped[float] = mapped_column(nullable=True)