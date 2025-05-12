from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON
from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Template(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # например: "hidden_work" или "commissioning"
    fields: Mapped[list[str]] = mapped_column(JSON, default=list)
