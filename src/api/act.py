from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.act import ActCreate, ActRead, ActUpdate
from core.dependencies.db import get_db_session
from crud.act import ActCRUD

router = APIRouter(prefix="/acts", tags=["Acts"])
crud = ActCRUD()

@router.post("/", response_model=ActRead)
async def create_act(act_in: ActCreate, db: AsyncSession = Depends(get_db_session)):
    return await crud.create(db, act_in)

@router.get("/", response_model=list[ActRead])
async def list_acts(db: AsyncSession = Depends(get_db_session)):
    return await crud.get_all(db)

@router.get("/{act_id}", response_model=ActRead)
async def get_act(act_id: int, db: AsyncSession = Depends(get_db_session)):
    act = await crud.get(db, act_id)
    if not act:
        raise HTTPException(404, detail="Act not found")
    return act

@router.put("/{act_id}", response_model=ActRead)
async def update_act(act_id: int, update_in: ActUpdate, db: AsyncSession = Depends(get_db_session)):
    act = await crud.get(db, act_id)
    if not act:
        raise HTTPException(404, detail="Act not found")
    return await crud.update(db, act, update_in)

@router.delete("/{act_id}", status_code=204)
async def delete_act(act_id: int, db: AsyncSession = Depends(get_db_session)):
    act = await crud.get(db, act_id)
    if not act:
        raise HTTPException(404, detail="Act not found")
    await crud.delete(db, act)
