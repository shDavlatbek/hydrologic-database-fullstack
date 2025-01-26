from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from pydantic import ValidationError
from api.auth import fastapi_users

from api.dependencies import UOWDep
from prediction.predictor import predict
from services.geo import GeoService, ParameterService, ParameterNameService
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


@router.get("/with_parameters")
async def get_wells_with_parameters(
    uow: UOWDep,
    date: datetime,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().get_wells_with_parameters(uow, date)


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
    
    # dates, gwl, rain, mint, maxt, avgt = await ParameterService().predict_parameters(uow, well_number)
    # predictions = predict(
    #     dates,
    #     well_number,
    #     gwl, 
    #     rain, 
    #     mint, 
    #     maxt, 
    #     avgt
    # )
    # return {'dates': dates[12:], 'predictions': predictions}
    return {'dates': [], 'predictions': []}


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


@router.get("/parameter/dates")
async def  get_parameter_dates(
    uow: UOWDep,
    user=Depends(fastapi_users.current_user(active=True))
):  
    return await ParameterService().get_parameter_dates(uow)


@router.post("/parameter/delete")
async def delete_parameter(
    uow: UOWDep,
    filters: ParameterQuery,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await ParameterService().delete_parameter(uow, filters)


@router.get("/{number}")
async def get_well(
    uow: UOWDep,
    number: int,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().get_well(uow, number)


@router.post("/{number}/upload")
async def upload_file(
    uow: UOWDep,
    number: int,
    file: UploadFile = File(...),
    user=Depends(fastapi_users.current_user(active=True))
):
    from pandas import read_excel
    df = read_excel(file.file)
    parameter_names = await ParameterNameService().get_parameters(uow)
    parameter_names = len([name.name for name in parameter_names]) + 1
    df = df.iloc[:, :parameter_names]
    # add empty columns if there are less columns than parameter names
    for i in range(parameter_names - df.shape[1]):
        df.insert(df.shape[1], f'empty_column_{i}', '')
    return {
        "filename": file.filename,
        "df": df.to_json(orient='records'),
        "content_type": file.content_type,
        "file_size": len(await file.read()),  # Read the file content to determine the size
    }


@router.post("/{number}/parameter/bulk-add")
async def bulk_add_parameter(
    uow: UOWDep,
    number: int,
    data: list[dict],
    user=Depends(fastapi_users.current_user(active=True))
):
    existing_parameters = []
    try: 
        for param_index, parameter in enumerate(data):
            for index, (key, value) in enumerate(parameter.items()):
                if index == 0:
                    continue
                else:
                    ParameterAdd(
                        well=number,
                        parameter_name=index,
                        value=value,
                        date=datetime.strptime(parameter['0'], '%Y/%m')
                    )
                    existing_parameter = await ParameterService().get_parameters(uow, 
                        filters={'date': datetime.strptime(parameter['0'], '%Y/%m'),
                                 'well': number,
                                 'parameter_name': index}
                    )
                    if existing_parameter:
                        existing_parameters.append(existing_parameter[0])
        return {"ok": True, "existing_parameters": existing_parameters}
    except (ValidationError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


@router.post("/{number}/parameter/bulk-add/confirmed")
async def bulk_add_parameter_confirmed(
    uow: UOWDep,
    number: int,
    data: list[dict],
    user=Depends(fastapi_users.current_user(active=True))
):
    try: 
        for param_index, parameter in enumerate(data):
            for index, (key, value) in enumerate(parameter.items()):
                if index == 0:
                    continue
                else:
                    param = ParameterAdd(
                        well=number,
                        parameter_name=index,
                        value=value,
                        date=datetime.strptime(parameter['0'], '%Y/%m')
                    )
                    await ParameterService().add_parameter(uow, param)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{number}/edit")
async def edit_well(
    uow: UOWDep,
    number: int,
    geo_well: AddGeoWell,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await GeoService().edit_well(uow, number, geo_well)