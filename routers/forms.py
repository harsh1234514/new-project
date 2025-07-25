from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime
import uuid

from database import get_db
from models import User, FormSubmission, FileAttachment
from schemas import (
    FormSubmissionCreate, FormSubmissionResponse, FormSubmissionUpdate,
    FormSubmissionWithAttachments, MessageResponse
)
from routers.auth import get_current_user

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/submit", response_model=FormSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_form(
    form_data: FormSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a new form."""
    db_form = FormSubmission(
        user_id=current_user.id,
        form_type=form_data.form_type,
        form_data=form_data.form_data
    )
    
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    
    return db_form

@router.get("/submissions", response_model=List[FormSubmissionResponse])
async def get_user_submissions(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all form submissions for the current user."""
    submissions = db.query(FormSubmission).filter(
        FormSubmission.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return submissions

@router.get("/submissions/{submission_id}", response_model=FormSubmissionWithAttachments)
async def get_submission_by_id(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific form submission by ID."""
    submission = db.query(FormSubmission).filter(
        FormSubmission.id == submission_id,
        FormSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form submission not found"
        )
    
    return submission

@router.put("/submissions/{submission_id}", response_model=FormSubmissionResponse)
async def update_submission(
    submission_id: int,
    form_update: FormSubmissionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a form submission."""
    submission = db.query(FormSubmission).filter(
        FormSubmission.id == submission_id,
        FormSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form submission not found"
        )
    
    # Update fields if provided
    if form_update.form_data is not None:
        submission.form_data = form_update.form_data
    if form_update.status is not None:
        submission.status = form_update.status
    
    db.commit()
    db.refresh(submission)
    
    return submission

@router.delete("/submissions/{submission_id}", response_model=MessageResponse)
async def delete_submission(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a form submission."""
    submission = db.query(FormSubmission).filter(
        FormSubmission.id == submission_id,
        FormSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form submission not found"
        )
    
    db.delete(submission)
    db.commit()
    
    return {"message": "Form submission deleted successfully"}

@router.post("/submissions/{submission_id}/upload", response_model=MessageResponse)
async def upload_file(
    submission_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file attachment to a form submission."""
    # Check if submission exists and belongs to current user
    submission = db.query(FormSubmission).filter(
        FormSubmission.id == submission_id,
        FormSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form submission not found"
        )
    
    # Validate file type and size
    allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.gif'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed"
        )
    
    # Check file size (max 10MB)
    max_file_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large (max 10MB)"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    # Create file attachment record
    db_attachment = FileAttachment(
        form_submission_id=submission_id,
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(file_content)
    )
    
    db.add(db_attachment)
    db.commit()
    
    return {"message": f"File {file.filename} uploaded successfully"}

@router.get("/types", response_model=List[str])
async def get_form_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all available form types."""
    # This would typically come from a configuration or database
    form_types = [
        "application_form",
        "feedback_form",
        "survey_form",
        "registration_form",
        "complaint_form"
    ]
    return form_types