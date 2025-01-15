from abc import ABC, abstractmethod
from typing import Type

from db.db import async_session_maker
from repositories.common import RegionRepository, DistrictRepository, LocationRepository
from repositories.geo import \
    GeoStationRepository, GeoWellRepository, \
    GeoOrganizationRepository, GeoWellTypeRepository, \
    ParameterNameRepository, ParameterRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    regions: Type[RegionRepository]
    districts: Type[DistrictRepository]
    location: Type[LocationRepository]
    
    # Geo
    parameter_name: Type[ParameterNameRepository]
    parameter: Type[ParameterRepository]
    geo_well: Type[GeoWellRepository]
    geo_organization: Type[GeoOrganizationRepository]
    geo_well_type: Type[GeoWellTypeRepository]
    geo_station: Type[GeoStationRepository]
    
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.regions = RegionRepository(self.session)
        self.districts = DistrictRepository(self.session)
        self.location = LocationRepository(self.session)
        
        # Geo
        self.geo_well = GeoWellRepository(self.session)
        self.parameter_name = ParameterNameRepository(self.session)
        self.parameter = ParameterRepository(self.session)
        self.geo_organization = GeoOrganizationRepository(self.session)
        self.geo_well_type = GeoWellTypeRepository(self.session)
        self.geo_station = GeoStationRepository(self.session) 

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow() -> UnitOfWork:
    uow = UnitOfWork() 
    return uow