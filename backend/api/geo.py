from datetime import datetime
from fastapi import APIRouter, Depends, Query
from api.auth import fastapi_users

from api.dependencies import UOWDep
from prediction.predictor import predict
from services.geo import GeoService, ParameterService
from schemas.geo import AddGeoWell, Parameter, ParameterQuery, ParameterAdd
from typing import Annotated, Optional
from dateutil.relativedelta import relativedelta


router = APIRouter(
    prefix="/geo",
    tags=["Geo"],
)


@router.get("/add")
async def add_well_form(
    uow: UOWDep,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().add_well_form(uow)


@router.post("/add")
async def add_well(
    uow: UOWDep,
    well: AddGeoWell,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().add_well(uow, well)


@router.get("/")
async def get_wells(
    uow: UOWDep,
    user=Depends(fastapi_users.current_user(active=True))
):
    res = []
    wells = await GeoService().get_wells(uow)
    for well in wells:
        res.append(await GeoService().get_well(uow, well.number))
    return res


@router.get("/parameter")
async def  get_parameters(
    uow: UOWDep,
    filters: Annotated[ParameterQuery, Query()],
    user=Depends(fastapi_users.current_user(active=True))
):
    filters = filters.model_dump(exclude_none=True)
    return await ParameterService().get_parameters(uow, filters)


@router.get("/parameter/predict")
async def get_predict(
    uow: UOWDep,
    well_number: int,
    user=Depends(fastapi_users.current_user(active=True))
):
    
    dates, gwl, rain, mint, maxt, avgt = await ParameterService().predict_parameters(uow, well_number)
    predictions = predict(
        dates,
        well_number,
        gwl, 
        rain, 
        mint, 
        maxt, 
        avgt
    )
    return {'dates': dates[12:], 'predictions': predictions}


@router.post("/parameter/add")
async def  add_parameter(
    uow: UOWDep,
    parameter: ParameterAdd,
    user=Depends(fastapi_users.current_user(active=True))
):
    return {"parameter_id": await ParameterService().add_parameter(uow, parameter)}


@router.post("/parameter/edit")
async def  edit_parameter(
    uow: UOWDep,
    parameter_id: int,
    parameter: ParameterAdd,
    user=Depends(fastapi_users.current_user(active=True))
):  
    await ParameterService().edit_parameter(uow, parameter_id, parameter)
    return {"ok": True}


@router.get("/{number}")
async def get_well(
    uow: UOWDep,
    number: int,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().get_well(uow, number)


@router.get("/{number}/edit")
async def get_well_edit(
    uow: UOWDep,
    number: int,
    geo_well: AddGeoWell,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().get_well_edit(uow, number, geo_well)