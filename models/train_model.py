from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = Path("data/raw/UCI_Credit_Card.csv")
MODEL_PATH = Path("models/model_v1.joblib")

TARGET = "default.payment.next.month"


def load_data(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)

    X = df.drop(columns=["ID", TARGET])
    y = df[TARGET]

    return X, y


def create_model() -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42,
            ),
        ),
    ])


def main():
    X, y = load_data(DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = create_model()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("Model evaluation:")
    print(f"Accuracy:  {accuracy_score(y_test, predictions):.4f}")
    print(f"Precision: {precision_score(y_test, predictions):.4f}")
    print(f"Recall:    {recall_score(y_test, predictions):.4f}")
    print(f"F1:        {f1_score(y_test, predictions):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, probabilities):.4f}")

    print("\nClassification report:")
    print(classification_report(y_test, predictions))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)


    #Сохранение модели
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()