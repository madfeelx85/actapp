from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, JSON
from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Act(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    build_object_id: Mapped[int] = mapped_column(
        ForeignKey("build_objects.id", ondelete="CASCADE")
    )
    template_id: Mapped[int] = mapped_column(
        ForeignKey("templates.id", ondelete="SET NULL")
    )

    data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    build_object = relationship("BuildObject", lazy="joined")
    template = relationship("Template", lazy="joined")
