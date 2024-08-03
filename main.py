"""FastAPI application for file upload operations."""

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException

app = FastAPI()


@app.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    """
    Upload and process a CSV file.

    Args:
        file (UploadFile): The CSV file to be uploaded.

    Returns:
        dict: A message indicating successful file upload.
    """
    csv_data = pd.read_csv(file.file)

    # Some operation with csv file

    return {"message": "File uploaded successfully."}


@app.post("/upload-excel")
def upload_excel(file: UploadFile = File(...)):
    """
    Upload and process an Excel file.

    Args:
        file (UploadFile): The Excel file to be uploaded.

    Returns:
        dict: A message indicating successful file upload.
    """
    excel_data = pd.read_excel(file.file)

    # Some operation with excel file

    return {"message": "File uploaded successfully."}


@app.post("/upload-file")
def upload_text_file(file: UploadFile = File(...)):
    """
    Upload and process a text file with size and type restrictions.

    Args:
        file (UploadFile): The text file to be uploaded.

    Returns:
        dict: A message indicating successful file upload.

    Raises:
        HTTPException: If the file is too large or not a .txt file.
    """
    max_file_size = 4 * 1024  # 4 KB

    if file.size > max_file_size:
        raise HTTPException(status_code=404, detail="File too large.")

    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=404, detail="File type not supported.")

    # Some operation with text file

    return {"message": "File uploaded successfully."}


@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    """
    Upload and process an image file with type restrictions.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A message indicating successful file upload.

    Raises:
        HTTPException: If the file type is not supported.
    """
    accepted_file_types = ["png", "jpg", "jpeg"]
    if file.content_type.split("/")[-1].lower() not in accepted_file_types:
        raise HTTPException(status_code=422, detail="File type not supported.")
    return {"message": "File uploaded successfully."}
