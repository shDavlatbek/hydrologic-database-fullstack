import sqlite3
import json
from datetime import datetime
db = sqlite3.connect('sqlite.db')
cursor = db.cursor()


def regions(): 
    regions = json.load(open('data/regions.json'))
    for region in regions:
        cursor.execute(
            'INSERT OR IGNORE INTO region (id, name) VALUES (?, ?)',
            (region['id'], region['name_uz'])
        )
  
def districts(): 
    districts = json.load(open('data/districts.json'))
    for district in districts:
        cursor.execute(
            'INSERT OR IGNORE INTO district (id, name, region_id) VALUES (?, ?, ?)',
            (district['id'], district['name_uz'], district['region_id'])
        )

def locations(): 
    locations = json.load(open('data/locations.json'))
    for location in locations:
        cursor.execute(
            'INSERT OR IGNORE INTO location (id, name) VALUES (?, ?)',
            (location['id'], location['name'])
        )
    
def geo_organizations(): 
    geo_organizations = json.load(open('data/geo_organizations.json'))
    for geo_organization in geo_organizations:
        cursor.execute(
            'INSERT OR IGNORE INTO geo_organization (id, name) VALUES (?, ?)',
            (geo_organization['id'], geo_organization['name'])
        )
    
def geo_stations(): 
    geo_stations = json.load(open('data/geo_stations.json'))
    for geo_station in geo_stations:
        cursor.execute(
            'INSERT OR IGNORE INTO geo_station (id, name) VALUES (?, ?)',
            (geo_station['id'], geo_station['name'])
        )

def geo_well_types(): 
    geo_well_types = json.load(open('data/geo_well_types.json'))
    for geo_well_type in geo_well_types:
        cursor.execute(
            'INSERT OR IGNORE INTO geo_welltype (id, name) VALUES (?, ?)',
            (geo_well_type['id'], geo_well_type['name'])
        )
    
def geo_well_parameters_names(): 
    geo_well_parameters_names = json.load(open('data/geo_parameter_names.json'))
    for geo_well_parameter_name in geo_well_parameters_names:
        cursor.execute(
            'INSERT OR IGNORE INTO parameter_name (id, name) VALUES (?, ?)',
            (geo_well_parameter_name['id'], geo_well_parameter_name['name'])
        )
    
def geo_wells(): 
    geo_wells = json.load(open('data/geo_wells.json'))
    for geo_well in geo_wells:
        cursor.execute(
            'INSERT OR IGNORE INTO geo_well (number, x, y, organization, region, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (geo_well['well'], geo_well['x'], geo_well['y'], 1, 9, datetime.now(), datetime.now())
        )

def geo_well_parameters(): 
    geo_well_parameters = json.load(open('data/geo_parameters.json'))
    for geo_well_parameter in geo_well_parameters:
        cursor.execute(
            'INSERT OR IGNORE INTO parameter (well, parameter_name, date, value) VALUES (?, ?, ?, ?)',
            (geo_well_parameter['well'], geo_well_parameter['parameter_name'], geo_well_parameter['date'], geo_well_parameter['value'])
        )

def melio_stations(): 
    melio_stations = json.load(open('data/melio_stations.json'))
    for melio_station in melio_stations:
        cursor.execute(
            'INSERT OR IGNORE INTO melio_station (id, name) VALUES (?, ?)',
            (melio_station['id'], melio_station['name'])
        )
        
def melio_well_types(): 
    melio_well_types = json.load(open('data/melio_well_types.json'))
    for melio_well_type in melio_well_types:
        cursor.execute(
            'INSERT OR IGNORE INTO melio_welltype (id, name) VALUES (?, ?)',
            (melio_well_type['id'], melio_well_type['name'])
        )
        
def melio_organizations(): 
    melio_organizations = json.load(open('data/melio_organizations.json'))
    for melio_organization in melio_organizations:
        cursor.execute(
            'INSERT OR IGNORE INTO melio_organization (id, name) VALUES (?, ?)',
            (melio_organization['id'], melio_organization['name'])
        )
        
if __name__ == '__main__':
    # regions()
    # districts()
    # locations()
    # geo_organizations()
    # geo_stations()
    # geo_well_types()
    # geo_well_parameters_names()
    # geo_wells()
    # geo_well_parameters()
    # melio_stations()
    # melio_well_types()
    melio_organizations()
    db.commit()
    db.close()