from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class BuildObject(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
