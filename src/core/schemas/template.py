from pydantic import BaseModel, Field


from core.enums.template_type import TemplateType


class TemplateBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = Field(default=None, max_length=500)
    path: str = Field(..., max_length=500)
    type: TemplateType
    fields: list[str] = Field(default_factory=list)


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(TemplateBase):
    pass


class TemplateRead(TemplateBase):
    id: int
    fields: list[str] = Field(default_factory=list)
