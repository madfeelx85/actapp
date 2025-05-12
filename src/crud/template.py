from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.template import Template
from core.schemas.template import TemplateCreate, TemplateUpdate


class TemplateCRUD:
    async def get(self, db: AsyncSession, id: int) -> Template | None:
        result = await db.execute(select(Template).where(Template.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Template]:
        result = await db.execute(select(Template))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: TemplateCreate) -> Template:
        obj = Template(**obj_in.dict())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(
        self, db: AsyncSession, db_obj: Template, update_in: TemplateUpdate
    ) -> Template:
        for field, value in update_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: Template) -> None:
        await db.delete(db_obj)
        await db.commit()
