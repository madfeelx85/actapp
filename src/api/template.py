import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.template import TemplateCreate, TemplateRead, TemplateUpdate
from core.dependencies.db import get_db_session
from crud.template import TemplateCRUD

router = APIRouter(prefix="/templates", tags=["Templates"])
UPLOAD_DIR = Path("src/static/templates")
crud = TemplateCRUD()

@router.post("/", response_model=TemplateRead)
async def create_template(template_in: TemplateCreate, db: AsyncSession = Depends(get_db_session)):
    return await crud.create(db, template_in)

@router.get("/", response_model=list[TemplateRead])
async def list_templates(db: AsyncSession = Depends(get_db_session)):
    return await crud.get_all(db)

@router.get("/{template_id}", response_model=TemplateRead)
async def get_template(template_id: int, db: AsyncSession = Depends(get_db_session)):
    obj = await crud.get(db, template_id)
    if not obj:
        raise HTTPException(404, detail="Template not found")
    return obj

@router.put("/{template_id}", response_model=TemplateRead)
async def update_template(template_id: int, update_in: TemplateUpdate, db: AsyncSession = Depends(get_db_session)):
    obj = await crud.get(db, template_id)
    if not obj:
        raise HTTPException(404, detail="Template not found")
    return await crud.update(db, obj, update_in)

@router.delete("/{template_id}", status_code=204)
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db_session)):
    obj = await crud.get(db, template_id)
    if not obj:
        raise HTTPException(404, detail="Template not found")
    await crud.delete(db, obj)


@router.post("/upload", response_model=TemplateRead)
async def upload_template_file(
    name: str = Form(...),
    description: str | None = Form(None),
    type: str = Form(...),  # "hidden_work" или "commissioning"
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
):
    # Проверка расширения
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Файл должен быть Excel (.xlsx или .xls)")

    # Создаём уникальное имя
    filename = f"{uuid4().hex}_{file.filename}"
    file_path = UPLOAD_DIR / filename

    # Сохраняем файл на диск
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Создаём Template
    new_template = await crud.create(
        db,
        obj_in=TemplateCreate(
            name=name,
            description=description,
            path=str(file_path),
            type=type,
        ),
    )

    return new_template