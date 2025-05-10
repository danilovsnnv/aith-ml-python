import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.middleware import AuthProxyMiddleware
from core.events import register_http_client_events

logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

app = FastAPI(title='API Gateway', description='Authentication gateway to check JWT token')

app.add_middleware(
    AuthProxyMiddleware,
    service_urls=settings.service_urls,
    auth_prefix=settings.auth_prefix
)
# CORS settings
app.add_middleware(
CORSMiddleware,
allow_origins=settings.allowed_origins,
allow_methods=["*"],
allow_headers=["*"],
allow_credentials=True,
)

register_http_client_events(app)
