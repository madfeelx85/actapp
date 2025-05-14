from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.dependencies.db import get_db_session
from core.models.build_object import BuildObject
from core.models.act import Act

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/objects/{build_object_id}/acts", response_class=HTMLResponse)
async def object_acts_page(
    request: Request, build_object_id: int, db: AsyncSession = Depends(get_db_session)
):
    build_object = await db.get(BuildObject, build_object_id)
    if not build_object:
        raise HTTPException(status_code=404, detail="Объект не найден")

    result = await db.execute(select(Act).where(Act.build_object_id == build_object_id))
    acts = result.scalars().all()

    return templates.TemplateResponse(
        "object_acts_page.html",
        {"request": request, "build_object": build_object, "acts": acts},
    )
