import tensorflow as tf
import pandas as pd
import joblib

# Load the model and pipeline
model = tf.keras.models.load_model('prediction/gwl_model.keras')
pipeline = joblib.load('prediction/pipeline.pkl')

def predict(dates, well_number, gwl, rain, mint, maxt, avgt):
    """
    Predict groundwater levels using the trained model.
    
    Parameters:
    - dates: list of dates in format 'YYYY/MM'
    - well_number: float, well identification number
    - gwl: list of ground water level measurements
    - rain: list of rainfall measurements (mm)
    - mint: list of minimum air temperatures (C)
    - maxt: list of maximum air temperatures (C)
    - avgt: list of average air temperatures (C)
    
    Returns:
    - list of predicted groundwater levels
    """
    # Create DataFrame from inputs
    data = {
        'Date': dates,
        'Well number': [well_number] * len(dates),
        'GWL (m)': gwl,
        'Rainfall mm': rain,
        'Min air temp. C': mint,
        'Max air temp. C': maxt,
        'Ave. air temp. C': avgt
    }
    df = pd.DataFrame(data)
    
    # Transform input columns using pipeline
    input_cols = ['Rainfall mm', 'Min air temp. C', 'Max air temp. C', 'Ave. air temp. C']
    df[input_cols] = pipeline.transform(df[input_cols])
    
    # Create sequential predictions
    def create_sequential_pred(model,well_chosen,start=0,end=12,timesteps=12):
        results=[]
        for i in range(timesteps):
            output=model.predict(well_chosen.iloc[start+i:end+i][['GWL (m)']+input_cols].values.reshape(1,12,5))
            results.append(float(output[0][0]))
        return results

    
    # Generate predictions
    predictions = create_sequential_pred(model, df)
    
    return predictions
