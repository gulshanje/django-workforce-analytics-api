import os
import joblib
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_store", "priority_model.joblib")

@lru_cache(maxsize=1)
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run train_model.py first.")
    return joblib.load(MODEL_PATH)

def predict_priority(text: str) -> str:
    model = load_model()
    prediction = model.predict([text])[0]
    return prediction