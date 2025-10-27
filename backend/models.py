from pydantic import BaseModel
from typing import Optional

class EmailListRequest(BaseModel):
    """Request model for listing emails"""
    max_results: int = 10
    query: str = ""


class EmailReadRequest(BaseModel):
    """Request model for reading an email"""
    email_id: str


class EmailSendRequest(BaseModel):
    """Request model for sending an email"""
    to: str
    subject: str
    body: str

class ChatMessage(BaseModel):
    """Request model for chat endpoint"""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    error: Optional[str] = None