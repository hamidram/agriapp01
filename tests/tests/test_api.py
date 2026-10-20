"""
Unit tests for the Agricultural Yield Intelligence FastAPI backend.
"""
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Ensure the root directory is in the python path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import your FastAPI app instance (adjust 'main' if your file is named differently, e.g., 'app.main')
try:
    from main import app
except ImportError:
    # Fallback if app is structured inside a package
    from src.main import app 

client = TestClient(app)

def test_read_root():
    """Test the root endpoint or health check if available."""
    response = client.get("/")
    # If you don't have a root GET endpoint, status 404 or 200 is fine depending on your main.py setup
    assert response.status_code in [200, 404]

def test_predict_endpoint_valid_payload():
    """Test the /predict endpoint with valid agricultural telemetry inputs."""
    payload = {
        "soil_moisture_pct": 30.0,
        "temperature_c": 24.0,
        "ph_level": 6.5,
        "rainfall_mm": 120.0
    }
    
    response = client.post("/predict", json=payload)
    
    # Verify the API responds successfully
    assert response.status_code == 200
    data = response.json()
    
    # Check that a prediction key is returned
    assert "prediction" in data