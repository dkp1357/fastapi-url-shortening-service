from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    short_code: str = Field(index=True, unique=True)
    created_at: datetime
    updated_at: datetime
    access_count: int = 0


class URLRequest(BaseModel):
    url: str
    length: Optional[int] = 6


class URLResponse(BaseModel):
    id: int | None
    url: str
    short_code: str
    created_at: datetime
    updated_at: datetime
    access_count: int = 0
