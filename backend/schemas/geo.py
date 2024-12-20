from typing import Optional, Union
from pydantic import BaseModel
from datetime import datetime
from schemas.common import CoordinateAdd


class AddGeoWell(BaseModel):
    number: int
    region: Optional[int] = None
    district: Optional[int] = None
    address: Optional[str] = None
    well_type: Optional[int] = None
    organization: Optional[int] = None
    location: Optional[int] = None
    station: Optional[int] = None
    coordinate: Optional[CoordinateAdd]
    

class GeoWell(BaseModel):
    id: int
    number: int
    region: Optional[int] = None
    district: Optional[int] = None
    organization: Optional[int] = None
    station: Optional[int] = None
    location: Optional[int] = None
    well_type: Optional[int] = None
    coordinate: Optional[int] = None
    address: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
        
class Parameter(BaseModel):
    id: int
    well: int
    parameter_name: int
    date: Optional[datetime] = None
    value: Optional[Union[float, int, str]] = None

    class Config:
        from_attributes = True
        
        

class ParameterAdd(BaseModel):
    well: int
    parameter_name: int
    date: Optional[datetime] = None
    value: Optional[Union[float, int, str]] = None

    class Config:
        from_attributes = True


class ParameterQuery(BaseModel):
    id: Optional[int] = None
    well: Optional[int] = None
    parameter_name: Optional[int] = None
    date: Optional[datetime] = None

    class Config:
        from_attributes = True