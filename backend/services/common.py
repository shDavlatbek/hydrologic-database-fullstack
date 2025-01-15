from schemas.common import Region, District
from utils.unitofwork import IUnitOfWork


class RegionService:
    async def get_regions(self, uow: IUnitOfWork):
        async with uow:
            regions = await uow.regions.find_all()
            return regions


class DistrictService:
    async def get_districts(self, uow: IUnitOfWork, region_id: int = None):
        async with uow:
            if region_id is None:
                return await uow.districts.find_all()
            return await uow.districts.find_all(filters={"region_id": region_id})
