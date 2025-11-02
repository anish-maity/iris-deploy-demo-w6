# iris_fastapi.py
#demo

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize FastAPI app
app = FastAPI(title="🌸 Iris Classifier API")

# Load the trained Decision Tree model
model = joblib.load("model.joblib")

# Define input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Classifier API!"}

# Prediction endpoint
@app.post("/predict/")
def predict_species(data: IrisInput):
    # Convert input data to a pandas DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Make prediction
    prediction = model.predict(input_df)[0]

    # Return the result
    return {"predicted_class": prediction}
