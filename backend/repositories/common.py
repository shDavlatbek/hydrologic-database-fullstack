from models.common import Region, District, Location
from utils.repository import SQLAlchemyRepository


class RegionRepository(SQLAlchemyRepository):
    model = Region


class DistrictRepository(SQLAlchemyRepository):
    model = District
    

class LocationRepository(SQLAlchemyRepository):
    model = Location