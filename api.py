from fastapi import FastAPI
from models.housing_model import HouseFeatures, PredictedPrice
from regression.random_forest_utils import RandomForestModelUtils

app = FastAPI()


@app.post("/predict")
def predict(features: HouseFeatures) -> PredictedPrice:
    rfmu = RandomForestModelUtils()
    price = rfmu.predict(features.district, features.rooms, features.square_meters)
    return PredictedPrice(price=price)