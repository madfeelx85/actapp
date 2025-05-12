from tempfile import template

from fastapi import APIRouter

from core.config import settings

from .build_object import router as build_object_router
from .template import router as template_router
from .act import router as act_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(
    build_object_router,
    template_router,
    act_router
)

