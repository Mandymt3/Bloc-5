import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import boto3
import mlflow

# mlflow experiment setup
EXPERIMENT_NAME='Getaround_pricing_optimization'
client = mlflow.tracking.MlflowClient()
mlflow.set_tracking_uri('https://getaround-mlflow-server.herokuapp.com/')
mlflow.set_experiment(EXPERIMENT_NAME)
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# call mlflow autolog
mlflow.sklearn.autolog()

# import data
df = pd.read_csv('/home/app/get_around_pricing_project.csv').iloc[:,1:]

# X,Y split
X = df.loc[:,[col for col in df.columns if col != 'rental_price_per_day']]
Y = df.rental_price_per_day

x_train,x_test,y_train,y_test = train_test_split(X,Y,random_state=42,test_size=0.2)

# preprocessing
numeric_features=[]
categorical_featues=[]

for col in X.columns:
    if X[col].dtype =='object':
        categorical_featues.append(X.columns.get_loc(col))
    else:
        numeric_features.append(X.columns.get_loc(col))

scaler = StandardScaler()
encoder = OneHotEncoder(drop='first')

preprocessor = ColumnTransformer(transformers=[('num',scaler,numeric_features),
                                        ('cat',encoder,categorical_featues)])

# Pipeline
model = Pipeline(steps=[
    ('preprocessing',preprocessor),
    ('Regressor', RandomForestRegressor(max_depth=15,n_estimators=200,min_samples_leaf=3))
])


#log experiment to mlflow
with mlflow.start_run():
    model.fit(x_train,y_train)

    accuracy = model.score(x_test,y_test)
    prediction = model.predict(x_test)

