# src/train.py
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
import pandas as pd

def train_model():
    # Set MLflow experiment name
    mlflow.set_experiment("agri_crop_prediction")

    with mlflow.start_run():
        print("Loading dataset...")
        # Simulated or loaded dataset
        data = pd.read_csv("data/crop_data.csv") if False else pd.DataFrame({
            'soil_moisture': [20, 40, 60, 80, 30, 50],
            'temperature': [15, 25, 30, 35, 20, 22],
            'yield_target': [0, 1, 1, 0, 0, 1]
        })

        X = data[['soil_moisture', 'temperature']]
        y = data['yield_target']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define hyperparameters
        n_estimators = 50
        max_depth = 5

        # Log parameters to MLflow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        print("Training model...")
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate model
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)

        # Log metrics to MLflow
        mlflow.log_metric("accuracy", acc)
        print(f"Model trained successfully with Accuracy: {acc:.2f}")

        # Log and register model artifact
        mlflow.sklearn.log_model(
            model,
            "crop_model",
            skops_trusted_types=["sklearn.tree._tree.Tree"],
)

if __name__ == "__main__":
    train_model()