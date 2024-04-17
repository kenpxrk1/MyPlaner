from .task import router as user_router
from .tag import router as tag_router

all_routers = [
    user_router,
    tag_router
]