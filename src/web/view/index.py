from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies.db import get_db_session
from core.models.build_object import BuildObject
from sqlalchemy import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(BuildObject))
    objects = result.scalars().all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "objects": objects}
    )
