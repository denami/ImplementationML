import pandas as pd

from models.model_loader import load_model


MODEL_PATH = "models/model_v1.joblib"
DATA_PATH = "data/raw/UCI_Credit_Card.csv"


model = load_model(MODEL_PATH)

df = pd.read_csv(DATA_PATH)

sample = df.drop(
    columns=["ID", "default.payment.next.month"]
).iloc[[0]]

prediction = model.predict(sample)[0]
probability = model.predict_proba(sample)[0, 1]

print(f"Prediction: {prediction}")
print(f"Default probability: {probability:.4f}")