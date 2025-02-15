from typing import Any, Dict, Optional, Set, Tuple, Union
from pydantic import BaseModel
from datetime import datetime, timedelta


class AddGeoWell(BaseModel):
    number: int
    region: Optional[int] = None
    district: Optional[int] = None
    address: Optional[str] = None
    well_type: Optional[int] = None
    organization: Optional[int] = None
    location: Optional[int] = None
    station: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    

class GeoWell(AddGeoWell):
    id: int
    created_at: datetime
    updated_at: datetime
    parameters: Optional[list['Parameter']] = None
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if not data.get("parameters"):  # Убираем поле, если оно None или []
            data.pop("parameters", None)
        return data

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
        

class ParameterCalculations(BaseModel):
    id: Optional[int] = None
    well: Optional[int] = None
    parameter_name: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @property
    def date(self) -> Tuple[Optional[datetime], Optional[datetime]]:
        return (self.start_date, self.end_date)

    class Config:
        from_attributes = True

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Dump the model to a dictionary while excluding keys with None values.
        Additionally, remove 'start_date' and 'end_date' and replace them with a
        'datetime' key whose value is a tuple of the non-None dates.
        """
        # Dump the model with `exclude_none=True` so that any field with a None value is omitted.
        data = super().model_dump(exclude_none=True, **kwargs)

        # Remove 'start_date' and 'end_date' from the dumped data (if present)
        data.pop("start_date", None)
        data.pop("end_date", None)

        if self.start_date and self.end_date:
            # Build the datetime tuple from the instance attributes, excluding None values.
            dt = tuple(x for x in (self.start_date, self.end_date + timedelta(days=1)) if x is not None)
            if dt:
                data["date"] = dt

        return data

