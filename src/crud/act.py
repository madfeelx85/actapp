from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.act import Act
from core.schemas.act import ActCreate, ActUpdate


class ActCRUD:
    async def get(self, db: AsyncSession, id: int) -> Act | None:
        result = await db.execute(select(Act).where(Act.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Act]:
        result = await db.execute(select(Act))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: ActCreate) -> Act:
        obj = Act(**obj_in.dict())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, db_obj: Act, update_in: ActUpdate) -> Act:
        for field, value in update_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: Act) -> None:
        await db.delete(db_obj)
        await db.commit()
