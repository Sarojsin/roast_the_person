"""
raost.py
API routes for roast generation.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os

from app.workers.worker import worker
from app.config import settings


router = APIRouter(prefix="/api")


@router.post("/roast")
async def create_roast(file: UploadFile = File(...)):
    """
    Upload a profile picture to be roasted.
    
    Args:
        file: Image file upload
        
    Returns:
        JSON with job_id for tracking
    """
    # Validate file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Submit job to worker
    try:
        job_id = worker.submit_job(content)
        
        return JSONResponse(
            status_code=202,  # Accepted
            content={
                "job_id": job_id,
                "message": "Roast job submitted successfully",
                "status_url": f"/api/roast/{job_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit roast job: {str(e)}"
        )


@router.get("/roast/{job_id}")
async def get_roast_status(job_id: str):
    """
    Check the status of a roast job.
    
    Args:
        job_id: Job identifier
        
    Returns:
        JSON with job status and result (if completed)
    """
    job_status = worker.get_job_status(job_id)
    
    if not job_status:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    return JSONResponse(content=job_status)
