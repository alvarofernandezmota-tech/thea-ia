import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

def train_intent_model():
    print("[INFO] Script de entrenamiento iniciado...")

    data_path = os.path.join(os.path.dirname(__file__), 'data')
    models_path = os.path.join(os.path.dirname(__file__), 'models')
    dataset_file = os.path.join(data_path, "intents_dataset.csv")

    print(f"[INFO] Cargando dataset: {dataset_file}")
    df = pd.read_csv(dataset_file)
    print(f"[INFO] Ejemplos cargados: {len(df)}")
    df = df.dropna(subset=['text'])
    df = df[df['text'].str.strip() != '']

    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1,2), stop_words='english')),
        ('clf', LinearSVC(C=1.0, class_weight='balanced', random_state=42, max_iter=2000))
    ])
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['intent'], test_size=0.2, random_state=42, stratify=df['intent']
    )
    print(f"[INFO] Entrenando con {len(X_train)} ejemplos...")
    model_pipeline.fit(X_train, y_train)
    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"[INFO] Precisión en test: {accuracy:.2%}")
    print(classification_report(y_test, y_pred))

    if not os.path.exists(models_path):
        os.makedirs(models_path)
    model_path = os.path.join(models_path, "model_intent.pkl")
    joblib.dump(model_pipeline, model_path)
    print(f"[INFO] Modelo guardado en: {model_path}")

if __name__ == "__main__":
    train_intent_model()
