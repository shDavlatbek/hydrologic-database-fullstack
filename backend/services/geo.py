from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, extract, select
from schemas.common import NameFieldAdd
from schemas.geo import AddGeoWell, Parameter, ParameterQuery
from utils.unitofwork import IUnitOfWork
from models.geo import Parameter as ParameterModel


class GeoService:
    async def add_well_form(self, uow: IUnitOfWork):
        async with uow:
            locations = await uow.location.find_all()
            organizations = await uow.geo_organization.find_all()
            well_types = await uow.geo_well_type.find_all()
            stations = await uow.geo_station.find_all()
            return {
                "locations": locations,
                "organizations": organizations,
                "well_types": well_types,
                "stations": stations
            }
    
    async def add_well(self, uow: IUnitOfWork, well: AddGeoWell):
        well_dict = well.model_dump()
        async with uow:
            well_id = await uow.geo_well.add_one(well_dict)
            await uow.commit()
            return well_id

    async def get_wells(self, uow: IUnitOfWork):
        async with uow:
            return await uow.geo_well.find_all()
        
    async def get_wells_with_parameters(self, uow: IUnitOfWork, date: datetime):
        async with uow:
            wells = await uow.geo_well.find_all()
            for well in wells:
                well.parameters = await uow.parameter.find_all(filters={'well': well.number, 'date': date.isoformat()})
            return wells
    
    async def get_well(self, uow: IUnitOfWork, well_number: int):
        async with uow:
            well = await uow.geo_well.find_one(number=well_number)
            if well:
                well.station = await uow.geo_station.find_one(id=well.station) if well.station else None
                well.organization = await uow.geo_organization.find_one(id=well.organization) if well.organization else None
                well.region = await uow.regions.find_one(id=well.region) if well.region else None
                well.district = await uow.districts.find_one(id=well.district) if well.district else None
                well.well_type = await uow.geo_well_type.find_one(id=well.well_type) if well.well_type else None
                well.location = await uow.location.find_one(id=well.location) if well.location else None
                return well
            else:
                return None
    
    async def edit_well(self, uow: IUnitOfWork, well_number: int, well: AddGeoWell):
        well_dict = well.model_dump()
        async with uow:
            await uow.geo_well.edit_one(well_dict, number=well_number)
            await uow.commit()
            
            
class ParameterNameService:
    async def add_parameter(self, uow: IUnitOfWork, parameter_name: NameFieldAdd):
        parameter_dict = parameter_name.model_dump()
        async with uow:
            parameter_id = await uow.parameter_name.add_one(parameter_dict)
            await uow.commit()
            return parameter_id
        
    async def get_parameters(self, uow: IUnitOfWork):
        async with uow:
            return await uow.parameter_name.find_all()

    
    async def edit_parameter(self, uow: IUnitOfWork, parameter_id: int, parameter_name: NameFieldAdd):
        parameter_name_dict = parameter_name.model_dump()
        async with uow:
            await uow.parameter_name.edit_one(parameter_id, parameter_name_dict)
            await uow.commit()
            

class ParameterService:
    async def add_parameter(self, uow: IUnitOfWork, parameter: Parameter):
        parameter_dict = parameter.model_dump()
        async with uow:
            parameter_id = await uow.parameter.add_one(parameter_dict)
            await uow.commit()
            return parameter_id
        
    async def get_parameters(self, uow: IUnitOfWork, filters):
        async with uow:
            if filters:
                return await uow.parameter.find_all(filters=filters)
            else:
                return await uow.parameter.find_all()
        
    async def predict_parameters(
        self, 
        uow: IUnitOfWork, 
        well_number: int,
    ):
        
        # print(all_months)
        async with uow:
            end_date = (await uow.parameter.find_all(filters={'well': well_number}, order_by='date', order_desc=True, limit=1))[0].date
            start_date = end_date - relativedelta(months=12)
            dates = [
                (start_date + relativedelta(months=i)).strftime("%Y/%m")
                for i in range(1, (end_date + relativedelta(months=12) - start_date).days // 30 + 1)
            ]
            gwl = await uow.parameter.find_all(filters={'parameter_name': 1, 'well': well_number, 'date': (start_date+relativedelta(months=1), end_date+relativedelta(months=1))}, order_by='date', order_desc=False)
            rainfall = await uow.parameter.find_all(filters={'parameter_name': 2, 'well': well_number, 'date': (start_date+relativedelta(months=1), end_date+relativedelta(months=1))}, order_by='date', order_desc=False)
            mint = await uow.parameter.find_all(filters={'parameter_name': 3, 'well': well_number, 'date': (start_date+relativedelta(months=1), end_date+relativedelta(months=1))}, order_by='date', order_desc=False)
            maxt = await uow.parameter.find_all(filters={'parameter_name': 4, 'well': well_number, 'date': (start_date+relativedelta(months=1), end_date+relativedelta(months=1))}, order_by='date', order_desc=False)
            avgt = await uow.parameter.find_all(filters={'parameter_name': 5, 'well': well_number, 'date': (start_date+relativedelta(months=1), end_date+relativedelta(months=1))}, order_by='date', order_desc=False)
            gwl_values = [item.value for item in gwl] + [0]*12
            rainfall_values = [item.value for item in rainfall] + [0]*12
            mint_values = [item.value for item in mint] + [0]*12
            maxt_values = [item.value for item in maxt] + [0]*12
            avgt_values = [item.value for item in avgt] + [0]*12
            
            print(len(dates), len(gwl_values), len(rainfall_values), len(mint_values), len(maxt_values), len(avgt_values), sep='\n\n')
            return dates, gwl_values, rainfall_values, mint_values, maxt_values, avgt_values
    
    async def get_parameter_dates(self, uow: IUnitOfWork):
        async with uow:
            start_date = (await uow.parameter.find_all(order_by='date', order_desc=False, limit=1))[0].date
            end_date = (await uow.parameter.find_all(order_by='date', order_desc=True, limit=1))[0].date
            return {'start_date': start_date, 'end_date': end_date}
            
    async def edit_parameter(self, uow: IUnitOfWork, parameter_id: int, parameter: Parameter):
        parameter_dict = parameter.model_dump()
        async with uow:
            await uow.parameter.edit_one(parameter_id, parameter_dict)
            await uow.commit()
            
    async def delete_parameter(self, uow: IUnitOfWork, filters: ParameterQuery):
        async with uow:
            await uow.parameter.delete_one(**filters.model_dump())
            await uow.commit()

