from models.geo import GeoWell, WellType, Organization, Station, Parameter, ParameterName, Lithology
from utils.repository import SQLAlchemyRepository


class GeoWellRepository(SQLAlchemyRepository):
    model = GeoWell


class GeoWellTypeRepository(SQLAlchemyRepository):
    model = WellType


class GeoOrganizationRepository(SQLAlchemyRepository):
    model = Organization


class GeoStationRepository(SQLAlchemyRepository):
    model = Station
    
    
class ParameterNameRepository(SQLAlchemyRepository):
    model = ParameterName
    

class ParameterRepository(SQLAlchemyRepository):
    model = Parameter
    
    
class LithologyRepository(SQLAlchemyRepository):
    model = Lithology
