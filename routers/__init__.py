from routers.commands.base_command import router as base_router
from routers.commands.user_command import router as user_router

from aiogram import Router

router = Router(name=__name__)

router.include_router(base_router)
router.include_router(user_router)