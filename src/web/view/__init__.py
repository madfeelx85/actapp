from fastapi import APIRouter

from core.config import settings

from .index import router as index_router
from .object_acts import router as object_acts_router
from .templates import router as templates_router
from .acts import router as acts_router


router = APIRouter()
router.include_router(index_router)
router.include_router(object_acts_router)
router.include_router(templates_router)

router.include_router(acts_router)