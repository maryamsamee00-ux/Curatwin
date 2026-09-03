import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import time

def generate_validation_data(n_samples=2000):
    np.random.seed(42)
    X, y = [], []
    for _ in range(n_samples):
        label = np.random.choice([0, 1, 2], p=[0.35, 0.35, 0.30])
        if label == 0:
            ppg_hrv = np.random.normal(70, 12)
            gsr = np.random.normal(3.0, 1.0)
            skin_temp = np.random.normal(36.5, 0.3)
            imu = np.random.normal(0.2, 0.1)
            self_report = np.random.normal(0.2, 0.15)
        elif label == 1:
            ppg_hrv = np.random.normal(45, 10)
            gsr = np.random.normal(5.5, 1.2)
            skin_temp = np.random.normal(36.8, 0.4)
            imu = np.random.normal(0.4, 0.15)
            self_report = np.random.normal(0.5, 0.15)
        else:
            ppg_hrv = np.random.normal(25, 8)
            gsr = np.random.normal(8.0, 1.5)
            skin_temp = np.random.normal(37.2, 0.5)
            imu = np.random.normal(0.6, 0.2)
            self_report = np.random.normal(0.8, 0.12)
        X.append([max(5, ppg_hrv), max(0.5, gsr), skin_temp, max(0, imu), np.clip(self_report, 0, 1)])
        y.append(label)
    return np.array(X), np.array(y)

print("=" * 60)
print("CuraTwin AI Stress Classification — Validation Report")
print("=" * 60)

X, y = generate_validation_data(2000)
labels = ['low', 'moderate', 'high']

print(f"\nDataset: {len(X)} synthetic samples")
print(f"Class distribution: low={sum(y==0)}, moderate={sum(y==1)}, high={sum(y==2)}")

start = time.time()
model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
model.fit(X, y)
train_time = time.time() - start
print(f"\nTraining time: {train_time:.2f}s")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
start = time.time()
cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
cv_time = time.time() - start

print(f"\n5-Fold Cross-Validation:")
print(f"  Accuracy: {cv_scores.mean()*100:.1f}% (+/- {cv_scores.std()*100:.1f}%)")
print(f"  Per-fold: {[f'{s*100:.1f}%' for s in cv_scores]}")
print(f"  CV time: {cv_time:.2f}s")

X_test, y_test = generate_validation_data(500)
np.random.seed(99)
y_pred = model.predict(X_test)

overall_acc = accuracy_score(y_test, y_pred) * 100
f1 = f1_score(y_test, y_pred, average='weighted') * 100

print(f"\nHold-out Test Set (500 samples):")
print(f"  Overall Accuracy: {overall_acc:.1f}%")
print(f"  Weighted F1-Score: {f1:.1f}%")

print(f"\nPer-Class Report:")
print(classification_report(y_test, y_pred, target_names=labels))

print("=" * 60)
print("DISCLAIMER: This model was trained on synthetic demo data.")
print("It is NOT a clinical tool. Real-world deployment requires")
print("validated physiological datasets and clinical review.")
print("=" * 60)

scenarios = [
    ("Very low stress", [85, 2.0, 36.3, 0.1, 0.1]),
    ("Moderate stress", [45, 5.5, 36.8, 0.4, 0.5]),
    ("High stress", [20, 9.0, 37.5, 0.7, 0.9]),
    ("Mixed signals", [55, 4.0, 36.6, 0.3, 0.3]),
]
print("\nScenario Testing:")
for name, features in scenarios:
    pred = model.predict([features])[0]
    conf = max(model.predict_proba([features])[0]) * 100
    print(f"  {name}: -> {labels[pred]} ({conf:.0f}% confidence)")
