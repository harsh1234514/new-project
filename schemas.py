from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    phone_number: str
    full_name: Optional[str] = None
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return v

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Form schemas
class FormSubmissionBase(BaseModel):
    form_type: str
    form_data: Dict[str, Any]

class FormSubmissionCreate(FormSubmissionBase):
    pass

class FormSubmissionResponse(FormSubmissionBase):
    id: int
    user_id: int
    status: str
    submission_date: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FormSubmissionUpdate(BaseModel):
    form_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

# File attachment schemas
class FileAttachmentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class FormSubmissionWithAttachments(FormSubmissionResponse):
    attachments: List[FileAttachmentResponse] = []

# Response schemas
class MessageResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None