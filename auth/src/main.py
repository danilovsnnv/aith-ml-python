from fastapi import FastAPI

from api.v1.auth import router as auth_router
from api.v1.platform import router as platform_router
from api.v1.profiles import router as profile_router

app = FastAPI(title="Auth & profile service")
app.include_router(auth_router)
app.include_router(platform_router)
app.include_router(profile_router)
