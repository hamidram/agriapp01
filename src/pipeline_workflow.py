# src/pipeline_workflow.py
from prefect import flow, task
from src.train import train_model

@task(retries=2, retry_delay_seconds=5)
def ingest_data_task():
    print("Step 1: Ingesting and validating agricultural data sources...")
    # Add data loading/checking logic here
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