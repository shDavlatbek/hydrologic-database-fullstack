import json
import pandas as pd

def load_parameters():
  df = pd.read_excel('input_data_gwl.xlsx')

  df.drop(columns=['Clay %', 'Silt %', 'Sand %', 'Permeability sm/day', 'Porosity %', 'Specific yield %', 'Field capacity mm', 'Bulk density g/cm3', 'Meteo station ID'], inplace=True)
  df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m')

  df.sort_values(by='Date', inplace=True)

  data = df.to_dict(orient='records')
  parameter_index = {
    'GWL (m)': 1,
    'Rainfall mm': 2,
    'Min air temp. C': 3,
    'Max air temp. C': 4,
    'Ave. air temp. C': 5
  }

  full_data = []

  i = 0
  k = 0

  while i < len(data):
      item = data[i]
      for key, value in item.items():
        if key in parameter_index:
          full_data.append({
            'id': k,
            'well': item['Well number'],
            'parameter_name': parameter_index[key],
            'date': item['Date'].strftime('%Y-%m-%dT00:00:00'),
            'value': value
          })
          k += 1
      i += 1

  with open('output_data.json', 'w') as f:
    json.dump(full_data, f)


def load_coordinates():
  df = pd.read_excel('Well coordinates.xlsx')
  df.drop(columns=['Well number'], inplace=True)
  df.rename(columns={'Well ID': 'well', 'X': 'x', 'Y': 'y'}, inplace=True)
  df.to_json('output_coordinates.json', orient='records')


if __name__ == '__main__':
  load_parameters()
  # load_coordinates()
