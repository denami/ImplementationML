from pathlib import Path

import joblib


def load_model(model_path: str | Path):
    """
    Load a trained ML model from a joblib file.

    Args:
        model_path: Path to the saved model.

    Returns:
        Loaded scikit-learn model.
    """
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    return joblib.load(model_path)