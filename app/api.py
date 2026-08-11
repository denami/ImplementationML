from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request

from models.model_loader import load_model


MODEL_PATH = Path("models/model_v1.joblib")

app = Flask(__name__)

model = load_model(MODEL_PATH)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": "v1"
    })


@app.post("/predict")
def predict():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    try:
        features = pd.DataFrame([data])

        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0, 1])

        return jsonify({
            "prediction": prediction,
            "default_probability": round(probability, 4),
            "model_version": "v1"
        })

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )