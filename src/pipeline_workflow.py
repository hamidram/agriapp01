# src/pipeline_workflow.py
from prefect import flow, task
from pathlib import Path
import pandas as pd

# Use relative import since both files reside inside the same 'src/' folder
try:
    from .train import train_model
except ImportError:
    from train import train_model


@task(retries=2, retry_delay_seconds=5)
def ingest_data_task():
    print("Step 1: Ingesting and validating agricultural data sources...")
    
    file_path = Path("data/crop_data.csv")
    
    # Check if file exists (crucial if DVC pull hasn't been run yet)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset missing at {file_path}. Make sure to run 'dvc pull' first!")
    
    # Load and validate basic structure
    df = pd.read_csv(file_path)
    print(f"Successfully loaded dataset! Total records: {len(df)}")
    print(f"Columns found: {list(df.columns)}")
    
    # Basic data validation check
    if df.empty:
        raise ValueError("The agricultural dataset is empty.")
        
    return True

@task
def training_task():
    print("Step 2: Starting MLflow tracked model training...")
    train_model()
    return "Training Complete"

@flow(name="Agricultural Intelligence Pipeline")
def main_flow():
    print("--- Starting Prefect Pipeline Execution ---")
    data_ready = ingest_data_task()
    if data_ready:
        result = training_task()
        print(f"Pipeline Result: {result}")

if __name__ == "__main__":
    main_flow()