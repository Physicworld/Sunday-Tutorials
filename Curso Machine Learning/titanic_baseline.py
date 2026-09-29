"""Modelo base para el Titanic: limpieza + validación cruzada.

Uso:  python titanic_baseline.py
Lee datasets/train_titanic.csv (junto a este script) e imprime la accuracy
media de una validación cruzada de 5 particiones.
"""
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA = Path(__file__).resolve().parent / "datasets" / "train_titanic.csv"
NUMERICAS = ["Age", "SibSp", "Parch", "Fare", "Pclass"]
CATEGORICAS = ["Sex", "Embarked"]


def construir_modelo():
    # Limpieza dentro del pipeline: los imputadores se ajustan solo con cada
    # partición de entrenamiento (sin fuga de datos hacia la validación).
    preproceso = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), NUMERICAS),
        ("cat", Pipeline([
            ("imputar", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), CATEGORICAS),
    ])
    return Pipeline([
        ("preproceso", preproceso),
        ("modelo", RandomForestClassifier(n_estimators=200, max_depth=5, random_state=0)),
    ])


def main():
    df = pd.read_csv(DATA)
    X, y = df[NUMERICAS + CATEGORICAS], df["Survived"]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    scores = cross_val_score(construir_modelo(), X, y, cv=cv, scoring="accuracy")
    print(f"Filas: {len(df)}  |  Referencia (predecir siempre 'no sobrevive'): {1 - y.mean():.3f}")
    print(f"Accuracy (CV 5 particiones): {scores.mean():.3f} ± {scores.std():.3f}")


if __name__ == "__main__":
    main()
