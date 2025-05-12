from pydantic import BaseModel, Field, ConfigDict


class BuildObjectBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = Field(default=None, max_length=500)

class BuildObjectCreate(BuildObjectBase):
    pass

class BuildObjectUpdate(BuildObjectBase):
    pass

class BuildObjectRead(BuildObjectBase):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

