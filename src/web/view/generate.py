# web/view/generate.py
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.templating import Jinja2Templates

from core.dependencies.db import get_db_session
from core.models.act import Act
from core.models.build_object import BuildObject
from utils.doc_generator import ActDocumentGenerator

from loguru import logger

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/generate", response_class=HTMLResponse)
async def generate_page(request: Request, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Act).order_by(Act.created_at.desc()))
    acts = result.scalars().all()
    return templates.TemplateResponse(
        "acts_generate_page.html", {"request": request, "acts": acts}
    )


@router.get("/generate/{act_id}")
async def generate_act_file(act_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Act).where(Act.id == act_id))
    act = result.scalar_one_or_none()
    if not act:
        raise HTTPException(status_code=404, detail="Акт не найден")

    result = await db.execute(
        select(BuildObject).where(BuildObject.id == act.build_object_id)
    )
    build_object = result.scalar_one_or_none()

    if not build_object:
        raise HTTPException(status_code=404, detail="Объект не найден")

    generator = ActDocumentGenerator(act, build_object)
    file_path = generator.save_to_file()

    logger.info(f"Генерация файла для акта ID {act_id} завершена: {file_path}")
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
