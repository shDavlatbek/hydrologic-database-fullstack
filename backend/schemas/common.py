from typing import Optional
from pydantic import Field, BaseModel


class Region(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class District(BaseModel):
    id: int
    name: str
    region_id: int

    class Config:
        from_attributes = True
        
        
class  NameField(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
        

class  NameFieldAdd(BaseModel):
    name: str