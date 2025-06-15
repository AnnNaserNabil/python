import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
from typing import Optional, Tuple

from app.core.config import settings

def save_upload_file(
    upload_file: UploadFile, 
    sub_dir: str = "",
    allowed_extensions: Optional[list] = None
) -> Tuple[str, str]:
    """
    Save an uploaded file to the uploads directory.
    
    Args:
        upload_file: The uploaded file object
        sub_dir: Subdirectory within the uploads directory
        allowed_extensions: List of allowed file extensions (e.g., ['.jpg', '.png'])
    
    Returns:
        Tuple of (file_path, file_url)
    """
    # Ensure the upload directory exists
    upload_dir = settings.UPLOAD_DIR / sub_dir
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate a unique filename
    file_ext = Path(upload_file.filename).suffix.lower()
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = upload_dir / file_name
    
    # Check file extension if allowed_extensions is provided
    if allowed_extensions and file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save the file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Generate a URL for the file
    file_url = f"/uploads/{sub_dir}/{file_name}" if sub_dir else f"/uploads/{file_name}"
    
    return str(file_path), file_url

def delete_file(file_path: str) -> bool:
    """
    Delete a file from the filesystem.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        bool: True if file was deleted, False if file didn't exist
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error deleting file {file_path}: {str(e)}")
        return False

def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return Path(filename).suffix.lower()

def is_file_allowed(filename: str, allowed_extensions: list) -> bool:
    """Check if a file has an allowed extension."""
    return get_file_extension(filename) in allowed_extensions

def get_file_size(file: UploadFile) -> int:
    """Get the size of an uploaded file in bytes."""
    # Move to the end of the file
    file.file.seek(0, 2)
    file_size = file.file.tell()
    # Reset file pointer to the beginning
    file.file.seek(0)
    return file_size

def validate_file_size(file: UploadFile, max_size: int = None) -> bool:
    """
    Validate that a file is not larger than the maximum allowed size.
    
    Args:
        file: The uploaded file
        max_size: Maximum file size in bytes. If None, uses settings.MAX_UPLOAD_SIZE
        
    Returns:
        bool: True if file size is valid
    """
    if max_size is None:
        max_size = settings.MAX_UPLOAD_SIZE
        
    file_size = get_file_size(file)
    return file_size <= max_size
