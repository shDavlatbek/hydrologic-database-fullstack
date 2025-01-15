from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.common import NameField, Region, District


class Region(Base):
    __tablename__ = "region"
    pydantic_model = Region
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)


class District(Base):
    __tablename__ = "district"
    pydantic_model = District
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    region_id: Mapped[int] = mapped_column(nullable=False)
    

class Location(Base):
    __tablename__ = "location"
    pydantic_model = NameField
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)