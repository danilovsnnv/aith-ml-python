import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.interact import router as interact_router
from api.v1.platform import router as platform_router
from api.v1.events import router as events_router
from core.config import settings

app = FastAPI(title="Event Collector API")

app.include_router(events_router)
app.include_router(platform_router)
app.include_router(interact_router)
