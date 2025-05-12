from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.build_object import (
    BuildObjectCreate,
    BuildObjectRead,
    BuildObjectUpdate,
)
from core.dependencies.db import get_db_session
from crud.build_object import BuildObjectCRUD

router = APIRouter(prefix="/build", tags=["Build Objects"])
crud = BuildObjectCRUD()


@router.post("/", response_model=BuildObjectRead)
async def create_object(
    obj_in: BuildObjectCreate, db: AsyncSession = Depends(get_db_session)
):
    return await crud.create(db, obj_in)


@router.get("/", response_model=list[BuildObjectRead])
async def list_objects(db: AsyncSession = Depends(get_db_session)):
    return await crud.get_all(db)


@router.get("/{object_id}", response_model=BuildObjectRead)
async def get_object(object_id: int, db: AsyncSession = Depends(get_db_session)):
    obj = await crud.get(db, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj


@router.put("/{object_id}", response_model=BuildObjectRead)
async def update_object(
    object_id: int,
    update_in: BuildObjectUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    obj = await crud.get(db, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return await crud.update(db, obj, update_in)


@router.delete("/{object_id}", status_code=204)
async def delete_object(object_id: int, db: AsyncSession = Depends(get_db_session)):
    obj = await crud.get(db, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    await crud.delete(db, obj)
