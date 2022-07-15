import uvicorn
from fastapi import FastAPI,File, UploadFile
import pandas as pd
import mlflow
from pydantic import BaseModel
from typing import Literal, List, Union



description = """
Pricing Optimization API helps GetAround to better predict vehicle rental price.

## Introduction Endpoints
Here you can try:
* `/`: **GET** request that display a simple default message
* `/intro`: **GET** request that display the introduction of company GetAround

## Preview

Here you can try:
* `/preview` **GET** show a few rows of your dataset
* `/unique-values` **GET** show a given column values in your dataset


## Machine Learning 

Here you can try:
* `/predict` **POST** request vehicle daily rental price predicted by machine learning
* `/batch-predict` **POST** where you can upload a file to get predictions for several cars

Check out documentation below for more information on each endpoint. 
"""


tags_metadata = [
     {
        "name": "Introduction Endpoints",
        "description": "Simple endpoints",
    },
    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset"
    },

    {
        "name": "Predictions",
        "description": "Endpoints that uses our Machine Learning model for predicting vehicle rental price"
    }
]


app = FastAPI(
    title="Pricing Optimization API",
    description=description,
    version="0.1",
    contact={
        "name": "GetAround Data Science Group"
    },
    openapi_tags=tags_metadata
)


class PricingFeatures(BaseModel):
    model_key: Literal['Citroën','Renault','BMW','Peugeot','Audi','Nissan','Mitsubishi','Mercedes','Volkswagen','Toyota',
    'SEAT','Subaru','Opel','Ferrari','PGO','Maserati','Suzuki','Porsche','Ford','KIA Motors','Alfa Romeo','Fiat',
    'Lexus','Lamborghini','Mini','Mazda','Honda','Yamaha'] = 'Citroën'
    mileage: int
    engine_power: int
    fuel: Literal['diesel', 'petrol', 'hybrid_petrol', 'electro']
    paint_color: Literal['black', 'grey', 'blue', 'white', 'brown', 'silver', 'red', 'beige','green', 'orange']
    car_type: Literal['estate', 'sedan', 'suv', 'hatchback', 'subcompact', 'coupe','convertible', 'van']
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Simply returns a welcome message
    """
    message = "Hello, this is the Pricing Optimization API.For more information, check out documentation of the api at `/docs`"
    return message


@app.get("/intro", tags=["Introduction Endpoints"])
async def introduction():
    """
    Simple introduction of the company GetAround
    """
    message = "GetAround is the Airbnb for cars.You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide."

    return message


@app.get("/preview", tags=["Preview"])
async def dataframe(rows: int=5):
    """
    Get a sample of your whole dataset. 
    <br />You can specify how many rows you want by specifying a value for `rows`, default is `5`
    """
    df = pd.read_csv('get_around_pricing_project.csv').iloc[:,1:]
    sample = df.sample(rows)
    return sample.to_json()


@app.get("/unique-values", tags=["Preview"])
async def unique_values(column: str='model_key'):
    """
    Get unique values from a given column.
    <br />You can specify the column you want by specifying the name for `column`, default is the first column `model_key`
    <br />The name of each column is shown below: 
    <br />'model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps','has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires', 'rental_price_per_day'
    """
    df = pd.read_csv('get_around_pricing_project.csv').iloc[:,1:]
    df = pd.Series(df[column].unique())

    return df.to_json()

@app.post("/predict",tags=["Machine Learning"])
async def predict(predictionFeatures: PricingFeatures):
    """
    Prediction of rental price per day for some given features.
    <br />Endpoint will return a dictionnary like this:

    ```
    {'prediction': PREDICTION_VALUE[0,1]}
    ```

    You need to give this endpoint all columns values as dictionnary, or form data.
    """
    # Read data 
    data = pd.DataFrame(dict(predictionFeatures), index=[0])

    # Log model from mlflow 
    logged_model = 's3://cours-demo/3/775af888095a4d1097dba069a94644d3/artifacts/model'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    prediction = loaded_model.predict(data)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


@app.post("/batch-predict", tags=["Machine Learning"])
async def batch_predict(file: UploadFile = File(...)):
    """
    Make prediction on a batch of observation. 
    <br />This endpoint accepts only **csv files** containing all the trained columns WITHOUT the target variable. 
    """
    # Read file 
    df = pd.read_csv(file.file)

    # Log model from mlflow 
    logged_model = 's3://cours-demo/3/775af888095a4d1097dba069a94644d3/artifacts/model'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    predictions = loaded_model.predict(df)

    response = {"prediction": predictions.tolist()}
    return response



if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0',port=4030)