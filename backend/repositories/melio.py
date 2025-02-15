from models.melio import MelioWell, WellType, Organization, Station, Parameter, ParameterName
from utils.repository import SQLAlchemyRepository


class MelioWellRepository(SQLAlchemyRepository):
    model = MelioWell


class MelioWellTypeRepository(SQLAlchemyRepository):
    model = WellType


class MelioOrganizationRepository(SQLAlchemyRepository):
    model = Organization


class MelioStationRepository(SQLAlchemyRepository):
    model = Station
    
    
class ParameterNameRepository(SQLAlchemyRepository):
    model = ParameterName
    

class ParameterRepository(SQLAlchemyRepository):
    model = Parameter