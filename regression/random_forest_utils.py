import joblib
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from models.housing_model import DISTRICTS

class RandomForestModelUtils:
    def __init__(self):
        self.encoder = OrdinalEncoder()
        district_arrays = [[d] for d in DISTRICTS]
        self.encoder.fit(district_arrays)

    def load_model(self):
        self.model = joblib.load("./regression/random_forest_houses.joblib")
    
    def predict(self, district: str, rooms: int, square_meters: float):
        # Load modal
        self.load_model()
        
        # Get district converted to number
        district = self.encoder.transform([[district]])[0][0]
        
        # Convert this data to numpy array
        features_np_array = np.array([district, rooms, square_meters])
        
        # Predict
        result = self.model.predict([features_np_array])[0]
        
        return result