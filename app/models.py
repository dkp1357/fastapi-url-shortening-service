from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


# Request Model
class URLRequest(BaseModel):
    url: HttpUrl
    length: Optional[int] = Field(default=6, ge=3, le=30)
    # length: Optional[int] = 6


# Response model
class URLResponse(BaseModel):
    id: int
    url: HttpUrl
    shortCode: str
    createdAt: datetime
    updatedAt: datetime
    accessCount: int = 0
