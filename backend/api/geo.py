import copy
from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, Query, File, Response, UploadFile
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from api.auth import fastapi_users

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import io

from api.dependencies import UOWDep
from prediction.predictor import predict
from services.geo import GeoService, ParameterService, ParameterNameService
from schemas.geo import AddGeoWell, Parameter, ParameterCalculations, ParameterQuery, ParameterAdd
from typing import Annotated, Optional
from dateutil.relativedelta import relativedelta

from pymannkendall import original_test as mk_test
import pandas as pd
import numpy as np
from utils.calculations import calculate_statistics


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


@router.get("/parameter/calculations")
async def edit_well(
    uow: UOWDep,
    filters: Annotated[ParameterCalculations, Query()],
    user=Depends(fastapi_users.current_user(active=True))
):
    print(filters.model_dump())
    parameters = await ParameterService().get_parameters(uow, filters.model_dump())
    parameters = [x.model_dump() for x in parameters]
    df = pd.DataFrame(parameters)

    # print(df)

    # Convert the date column to datetime and extract year and month
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Map month numbers to Roman numerals
    month_mapping = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
        7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
    }
    df['month_roman'] = df['month'].map(month_mapping)

    # Pivot the DataFrame so that rows are years and columns are the months
    pivot_df = df.pivot(index='year', columns='month_roman', values='value').reset_index()

    # Optionally, reindex the columns to ensure the proper order
    cols_order = ['year', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
    pivot_df = pivot_df.reindex(columns=cols_order)

    
    # Convert the pivot table to a list of dictionaries
    df = pivot_df
    filtered_df = copy.deepcopy(df)
    stats, mk_results, cv = calculate_statistics(df)

    variance_row = {'year': 'Variance', **stats['Variance']}
    std_dev_row = {'year': 'Standard Deviation', **stats['Standard Deviation']}
    cv_row = {'year': 'Coefficient of Variation', **cv}
    
    variance_row_df = pd.DataFrame([variance_row])
    std_dev_row_df = pd.DataFrame([std_dev_row])
    cv_row_df = pd.DataFrame([cv_row])
    mk_rows = [pd.DataFrame([{**{'year': metric}, **values}]) for metric, values in mk_results.items()]
    
    # Combine dataframes with stats and Mann-Kendall test results
    
    all_time_stats = {
        'min': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min().min(),
        'max': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max().max(),
        'avg': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean().mean(),
        'variance': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].var().var(),
        'std_dev': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().std(),
        'cv': str(round((df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().std() / 
                          df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean().mean() * 100), 2)) + '%'
    }
    
    
    
    df = pd.concat([df, variance_row_df, std_dev_row_df, cv_row_df, *mk_rows], ignore_index=True)

    return {
        'success': True,
        'data': json.loads(df.to_json(orient='records')),
        # 'start_year': start_year,
        # 'end_year': end_year,
        # 'start_month': start_month,
        # 'end_month': end_month,
        'all_time_min': all_time_stats['min'],
        'all_time_max': all_time_stats['max'],
        'all_time_avg': round(all_time_stats['avg'], 2),
        'all_time_variance': round(all_time_stats['variance'], 2),
        'all_time_std_dev': round(all_time_stats['std_dev'], 2),
        'all_time_cv': all_time_stats['cv'],
        'filtered_df': json.loads(filtered_df.to_json(orient='records'))
    }
    
    
@router.get("/parameter/heatmap")
async def edit_well(
    uow: UOWDep,
    filters: Annotated[ParameterCalculations, Query()],
    user=Depends(fastapi_users.current_user(active=True))
):
    filters = filters.model_dump()
    parameters = await ParameterService().get_parameters(uow, filters)
    parameters = [x.model_dump() for x in parameters]
    df = pd.DataFrame(parameters)

    print(df)

    # Convert the date column to datetime and extract year and month
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Map month numbers to Roman numerals
    month_mapping = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
        7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
    }
    df['Oylar'] = df['month'].map(month_mapping)

    # Pivot the DataFrame so that rows are years and columns are the months
    pivot_df = df.pivot(index='year', columns='Oylar', values='value').reset_index()

    # Optionally, reindex the columns to ensure the proper order
    cols_order = ['year', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
    pivot_df = pivot_df.reindex(columns=cols_order)
    
    df = pivot_df
    matplotlib.use('agg')
    plt.figure(figsize=(len(df), 8), dpi=480)        
    try:
        sns.heatmap(df.set_index('year').T, annot=True, fmt=".1f", cmap="Blues", cbar=True,) # xticklabels=True, yticklabels=True  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # title and labels
    plt.title('Heatmap - ' + str(filters['well']))
    plt.xlabel('Yillar')
    plt.ylabel('Oylar')        
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=480)
    plt.close()
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": 'attachment; filename="heatmap.png"'}
    )
    


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