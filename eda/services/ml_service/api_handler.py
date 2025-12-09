import pickle
import pandas as pd
from pathlib import Path

class FastAPIHandler:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        try:
            model_path = Path(__file__).parent / "models" / "model.pkl"
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            print("Model loaded successfully in handler")
        except Exception as e:
            print(f"Error loading model in handler: {e}")
            self.model = None
    
    def predict(self, input_data):
        if self.model is None:
            raise ValueError("Model not loaded")
        
        features = pd.DataFrame([input_data])
        prediction = self.model.predict(features)[0]
        return float(prediction)