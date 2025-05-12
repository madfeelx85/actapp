from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.build_object import BuildObject
from core.schemas.build_object import BuildObjectCreate, BuildObjectUpdate

class BuildObjectCRUD:
    async def get(self, db: AsyncSession, id: int) -> BuildObject | None:
        result = await db.execute(select(BuildObject).where(BuildObject.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[BuildObject]:
        result = await db.execute(select(BuildObject))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: BuildObjectCreate) -> BuildObject:
        obj = BuildObject(**obj_in.dict())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, db_obj: BuildObject, update_in: BuildObjectUpdate) -> BuildObject:
        for field, value in update_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: BuildObject) -> None:
        await db.delete(db_obj)
        await db.commit()
