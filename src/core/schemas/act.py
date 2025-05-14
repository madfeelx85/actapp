from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime


class ActBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = Field(default=None, max_length=500)
    build_object_id: int
    template_id: int
    data: dict = Field(default_factory=dict)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(None),
        build_object_id: int = Form(...),
        template_id: int = Form(...),
        data: str = Form("{}"),  # приходит️ строка, потом нужно преобразовать в dict
    ):
        import json

        return cls(
            name=name,
            description=description,
            build_object_id=build_object_id,
            template_id=template_id,
            data=json.loads(data),
        )


class ActCreate(ActBase):
    pass


class ActUpdate(ActBase):
    pass


class ActRead(ActBase):
    id: int
    created_at: datetime
