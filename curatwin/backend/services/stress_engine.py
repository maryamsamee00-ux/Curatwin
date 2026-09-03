import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from ..config import MODEL_STORE_PATH

MODEL_FILE = os.path.join(MODEL_STORE_PATH, "stress_model_v1.joblib")
MODEL_VERSION = "1.0.0"

_model = None


def get_model():
    global _model
    if _model is None:
        try:
            _model = joblib.load(MODEL_FILE) if os.path.exists(MODEL_FILE) else None
        except Exception:
            _model = None  # sklearn version drift, corrupt file, ...
        if _model is None:
            _model = _create_baseline_model()
    return _model


def _create_baseline_model():
    """Create a baseline model for development/demo use."""
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8)
    np.random.seed(42)
    n_samples = 3000
    ppg_hrv = np.random.normal(50, 20, n_samples)
    gsr = np.random.normal(5, 2, n_samples)
    skin_temp = np.random.normal(36.5, 0.5, n_samples)
    imu = np.random.normal(0.3, 0.2, n_samples)
    self_report = np.random.uniform(0, 1, n_samples)
    stress_score = (
        (100 - np.clip(ppg_hrv, 0, 100)) * 0.3 +
        np.clip(gsr, 0, 10) * 5 +
        (37.5 - skin_temp) * 20 +
        np.clip(imu, 0, 1) * 10 +
        self_report * 30
    )
    labels = np.where(stress_score < 40, "low", np.where(stress_score < 65, "moderate", "high"))
    X = np.column_stack([ppg_hrv, gsr, skin_temp, imu, self_report])
    model.fit(X, labels)
    try:
        os.makedirs(MODEL_STORE_PATH, exist_ok=True)
        if os.access(MODEL_STORE_PATH, os.W_OK):
            joblib.dump(model, MODEL_FILE)
    except OSError:
        pass
    return model


def predict_stress(ppg_hrv, gsr_amplitude, skin_temp, imu_activity, self_report_stress):
    model = get_model()
    features = np.array([[ppg_hrv, gsr_amplitude, skin_temp, imu_activity, self_report_stress]])
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    class_idx = list(model.classes_).index(prediction)
    confidence = float(probabilities[class_idx])
    # numpy.str_ / numpy.float64 are NOT exact str/float; psycopg2 adapts by
    # exact type and rejects them. SQLite tolerated this, Postgres will not.
    return (
        str(prediction),
        float(confidence),
        MODEL_VERSION,
        "ppg_hrv,gsr_amplitude,skin_temp,imu_activity,self_report_stress",
    )
