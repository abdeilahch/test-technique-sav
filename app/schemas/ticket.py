from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List
import html


class TicketStatus(str, Enum):
    open = "open"
    stalled = "stalled"
    closed = "closed"


class TicketBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)

class TicketCreate(TicketBase):
    @field_validator("title", "description", mode="before")
    def escape_html(cls, v):
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        return html.escape(v).strip()

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator("title", "description", mode="before")
    def escape_html(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        return html.escape(v).strip()

class TicketRead(TicketBase):
    id: int
    status: TicketStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TicketsPagination(BaseModel):
    total: int
    total_pages: int
    current_page: int
    per_page: int
    tickets: List[TicketRead]
