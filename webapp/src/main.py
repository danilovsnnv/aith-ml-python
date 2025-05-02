import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware

from api.v1.webapp import router as webapp_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.include_router(webapp_router)
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

TOP_K = 12

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
