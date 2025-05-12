from pydantic import BaseModel, Field
from datetime import datetime


class ActBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = Field(default=None, max_length=500)
    build_object_id: int
    template_id: int
    data: dict = Field(default_factory=dict)


class ActCreate(ActBase):
    pass


class ActUpdate(ActBase):
    pass


class ActRead(ActBase):
    id: int
    created_at: datetime
