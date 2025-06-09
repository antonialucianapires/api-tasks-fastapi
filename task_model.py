from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=5, max_length=200)
    is_active: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

