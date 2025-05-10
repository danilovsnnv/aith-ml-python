import uvicorn
from fastapi import FastAPI

from api.v1.rec import router as rec_router
from api.v1.platform import router as platform_router

app = FastAPI(title="Recommendation Service API")

app.include_router(platform_router)
app.include_router(rec_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)