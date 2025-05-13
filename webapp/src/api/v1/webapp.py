import logging
import os

from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates

# Ensure logs directory exists
os.makedirs('/logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("/logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/profile", response_class=Response, include_in_schema=False)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})
