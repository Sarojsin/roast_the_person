"""
Tests for the roast API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create a simple test image
    img = Image.new('RGB', (500, 500), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Roast My Profile API"
    assert data["status"] == "running"


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_upload_valid_image(client, sample_image):
    """Test uploading a valid image."""
    files = {"file": ("test.jpg", sample_image, "image/jpeg")}
    response = client.post("/api/roast", files=files)
    
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert "status_url" in data


def test_upload_invalid_file_type(client):
    """Test uploading an invalid file type."""
    files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    response = client.post("/api/roast", files=files)
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_upload_oversized_file(client):
    """Test uploading a file that's too large."""
    # Create a large fake file
    large_data = b"x" * (11 * 1024 * 1024)  # 11MB
    files = {"file": ("large.jpg", io.BytesIO(large_data), "image/jpeg")}
    response = client.post("/api/roast", files=files)
    
    assert response.status_code == 400
    assert "too large" in response.json()["detail"]


def test_get_nonexistent_job(client):
    """Test getting a job that doesn't exist."""
    response = client.get("/api/roast/nonexistent-job-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_upload_and_check_status(client, sample_image):
    """Test the full flow of uploading and checking status."""
    # Upload image
    files = {"file": ("test.jpg", sample_image, "image/jpeg")}
    upload_response = client.post("/api/roast", files=files)
    assert upload_response.status_code == 202
    
    job_id = upload_response.json()["job_id"]
    
    # Check status
    status_response = client.get(f"/api/roast/{job_id}")
    assert status_response.status_code == 200
    
    status_data = status_response.json()
    assert "status" in status_data
    assert status_data["status"] in ["pending", "processing", "completed", "failed"]
