import os
from uuid import uuid4
from pathlib import Path

from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.db import get_db_session
from core.models.template import Template
from core.schemas.template import TemplateCreate
from core.enums.template_type import TemplateType
from crud.template import TemplateCRUD
from utils.template_parser import extract_fields_from_excel


router = APIRouter(prefix="/templates")
templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = Path("output/templates")
crud = TemplateCRUD()

@router.get("/", response_class=HTMLResponse)
async def template_list(request: Request, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Template))
    templates_list = result.scalars().all()

    return templates.TemplateResponse(
        "templates_list.html",
        {"request": request, "templates": templates_list}
    )

@router.get("/upload-form")
async def upload_template_form(request: Request):
    return templates.TemplateResponse(
        "template_upload_form.html",
        {"request": request,
        "template_types": list(TemplateType)},
    )

@router.post("/upload")
async def upload_template_file(
    name: str = Form(...),
    description: str | None = Form(None),
    type: TemplateType = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="Файл должен быть Excel (.xlsx или .xls)"
        )

    filename = f"{uuid4().hex}_{file.filename}"
    file_path = UPLOAD_DIR / filename
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    #  ПАРСИМ ПОЛЯ
    try:
        fields = extract_fields_from_excel(file_path)
        print(f"[TEMPLATE UPLOAD] Найдены поля: {fields}")  # <-- вот лог
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка чтения шаблона: {str(e)}")

    # СОХРАНЯЕМ шаблон
    new_template = await crud.create(
        db,
        obj_in=TemplateCreate(
            name=name,
            description=description,
            path=str(file_path),
            type=type,
            fields=fields,
        ),
    )

    print(f"[TEMPLATE UPLOAD] Шаблон успешно сохранён: {new_template.id}")
    return RedirectResponse(url="/templates", status_code=303)
