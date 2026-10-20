# src/train.py
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib
from pathlib import Path

def save_model(model, model_path: str):
    """Save the trained model to a specified path."""
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def train_model():
    # Set MLflow experiment name
    mlflow.set_experiment("agri_crop_prediction")

    with mlflow.start_run():
        print("Loading dataset...")
        # Load the real dataset generated in Week 1
        data_path = Path("data/crop_data.csv")
        if not data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {data_path}. Run 'dvc pull' first!")
        
        data = pd.read_csv(data_path)

        # Ensure target variable exists (mapping yield_target or classification label)
        # Note: If your CSV has 'crop_yield_tha' (continuous), convert to binary or use a Classifier/Regressor accordingly.
        # Here we create a dummy target if 'yield_target' isn't in the CSV column list:
        if 'yield_target' not in data.columns:
            # For demonstration, create a binary target based on yield threshold
            data['yield_target'] = (data['crop_yield_tha'] > data['crop_yield_tha'].median()).astype(int)

        # Exact feature names matching API schema and model expectation
        feature_columns = ['soil_moisture_pct', 'temperature_c', 'ph_level', 'rainfall_mm']
        
        X = data[feature_columns]
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

        # Log and register model artifact in MLflow
        mlflow.sklearn.log_model(
            model,
            "crop_model",
            skops_trusted_types=["sklearn.tree._tree.Tree"],
        )
        
        # Save model locally for FastAPI / Docker
        save_model(model, "models/model.pkl")

        return model

if __name__ == "__main__":
    train_model()