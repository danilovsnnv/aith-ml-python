from fastapi import FastAPI

from api.v1.auth import router as auth_router
from api.v1.platform import router as platform_router
from api.v1.user import router as user_router

app = FastAPI(title="User service API")
app.include_router(auth_router)
app.include_router(platform_router)
app.include_router(user_router)