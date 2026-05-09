import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv("/app/data/Obesity.csv")

cols_to_round = ["FCVC", "NCP", "CH2O", "FAF", "TUE"]

for col in cols_to_round:
    df[col] = df[col].round()

X = df.drop("Obesity", axis=1)
y = df["Obesity"]

categorical_features = [
    "Gender",
    "family_history",
    "FAVC",
    "CAEC",
    "SMOKE",
    "SCC",
    "CALC",
    "MTRANS"
]

numeric_features = [
    "Age",
    "Height",
    "Weight",
    "FCVC",
    "NCP",
    "CH2O",
    "FAF",
    "TUE"
]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Acurácia: {accuracy:.4f}")
print(classification_report(y_test, y_pred))

os.makedirs("/model_data", exist_ok=True)

joblib.dump(pipeline, "/model_data/obesity_model.pkl")

with open("/model_data/metrics.txt", "w", encoding="utf-8") as file:
    file.write(f"Acurácia: {accuracy:.4f}\n\n")
    file.write(classification_report(y_test, y_pred))

print("Modelo salvo em /model_data/obesity_model.pkl")
print("Métricas salvas em /model_data/metrics.txt")