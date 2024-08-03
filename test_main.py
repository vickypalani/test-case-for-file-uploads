"""Test module for the main application."""

from io import BytesIO

import pandas as pd
from fastapi.testclient import TestClient
from PIL import Image

from main import app

client = TestClient(app)


def create_sample_csv():
    """Create a sample CSV file for testing."""
    sample_data = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
    csv_buffer = BytesIO()
    sample_data.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer


def create_sample_excel():
    """Create a sample Excel file for testing."""
    sample_data = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
    excel_buffer = BytesIO()
    sample_data.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    return excel_buffer


def create_dummy_file(size_in_bytes: int, filename: str = "dummy.txt"):
    """Create a dummy file with specified size and name."""
    file_buffer = BytesIO()
    file_buffer.write(b"0" * size_in_bytes)
    file_buffer.name = filename
    file_buffer.seek(0)
    return file_buffer


def create_dummy_image(file_type: str = "jpeg"):
    """Create a dummy image file."""
    image_buffer = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(image_buffer, file_type)
    image_buffer.name = "dummy." + file_type
    image_buffer.seek(0)
    return image_buffer


def test_csv_upload():
    """Test CSV file upload endpoint."""
    response = client.post("/upload-csv", files={"file": create_sample_csv()})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully."}


def test_excel_upload():
    """Test Excel file upload endpoint."""
    response = client.post("/upload-excel", files={"file": create_sample_excel()})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully."}


def test_file_upload_success():
    """Test successful file upload."""
    response = client.post("/upload-file", files={"file": create_dummy_file(1024 * 1)})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully."}


def test_file_upload_failure():
    """Test file upload failures due to size and type restrictions."""
    # Test file size limit
    oversized_file_response = client.post(
        "/upload-file", files={"file": create_dummy_file(1024 * 8)}
    )
    assert oversized_file_response.status_code == 404
    assert oversized_file_response.json() == {"detail": "File too large."}

    # Test file type restriction
    unsupported_file_response = client.post(
        "/upload-file", files={"file": create_dummy_file(1024 * 2, "dummy.jpg")}
    )
    assert unsupported_file_response.status_code == 404
    assert unsupported_file_response.json() == {"detail": "File type not supported."}


def test_image_upload_success():
    """Test successful image upload."""
    response = client.post("/upload-image", files={"file": create_dummy_image(file_type="png")})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully."}

def test_image_upload_failure():
    """Test image upload failure due to type restriction."""
    response = client.post("/upload-image", files={"file": create_dummy_image(file_type="gif")})
    assert response.status_code == 422
    assert response.json() == {"detail": "File type not supported."}
