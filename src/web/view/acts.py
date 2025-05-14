from datetime import datetime, timezone

from fastapi import APIRouter, Request, Depends, Query, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from core.dependencies.db import get_db_session
from core.models.act import Act
from core.models.template import Template
from core.models.build_object import BuildObject

from utils.template_parser import extract_fields_from_excel

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/acts/create", response_class=HTMLResponse)
async def create_act_page(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    # Получаем все шаблоны и объекты строительства
    templates_result = await db.execute(select(Template))
    templates_list = templates_result.scalars().all()

    objects_result = await db.execute(select(BuildObject))
    build_objects_list = objects_result.scalars().all()

    return templates.TemplateResponse(
        "acts/create_act.html",
        {
            "request": request,
            "templates": templates_list,
            "build_objects": build_objects_list
        }
    )

@router.get("/acts/form", response_class=HTMLResponse)
async def get_act_dynamic_form(
    request: Request,
    template_id: int = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    template = await db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")

    # Можно считать поля напрямую из шаблона, либо взять из базы (если они там уже сохранены при загрузке шаблона)
    fields = template.fields or []

    return templates.TemplateResponse(
        "partials/act_dynamic_form.html",
        {
            "request": request,
            "fields": fields,
        }
    )

@router.post("/acts/create", response_class=HTMLResponse)
async def create_act_from_form(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
):
    form = await request.form()
    form_data = dict(form)

    # Извлекаем служебные поля
    build_object_id = int(form_data.pop("build_object_id"))
    template_id = int(form_data.pop("template_id"))
    name = form_data.pop("name", f"Акт от {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
    description = form_data.pop("description", "")

    # Остальное — пользовательские данные
    data = form_data

    new_act = Act(
        name=name,
        description=description,
        build_object_id=build_object_id,
        template_id=template_id,
        data=data
    )
    db.add(new_act)
    await db.commit()

    return RedirectResponse(url=f"/objects/{build_object_id}/acts", status_code=303)