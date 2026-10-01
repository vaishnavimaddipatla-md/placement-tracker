from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr

Status = Literal["Wishlist", "Applied", "Online Test", "Interview", "Offer", "Rejected"]


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ApplicationCreate(BaseModel):
    company: str
    role: str
    job_link: Optional[str] = None
    location: Optional[str] = None
    status: Status = "Wishlist"
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    job_link: Optional[str] = None
    location: Optional[str] = None
    status: Optional[Status] = None
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    job_link: Optional[str]
    location: Optional[str]
    status: str
    applied_date: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}