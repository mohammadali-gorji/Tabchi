import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "ml_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

def train_model(csv_file="data.csv"):
    """
    Read from CSV
    """
    df = pd.read_csv(csv_file)
    texts = df["text"]
    labels = df["label"]

    vectorizer = TfidfVectorizer(max_features=3000)
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression()
    model.fit(X, labels)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Saved Model.")


def load_model():
    """
    Upload and Process File
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Error")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def predict_message(text: str) -> bool:
    """
    True / False
    """
    model, vectorizer = load_model()
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    return prediction == 1

if __name__ == "__main__":
    try:
        train_model("data.csv")
    except Exception as e:
        print("Error in model learning: ", e)
