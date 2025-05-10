import httpx
from fastapi import FastAPI


def register_http_client_events(app: FastAPI):
    """
    Registers startup and shutdown events to manage a shared HTTPX AsyncClient.
    """
    @app.on_event("startup")
    async def startup_http_client():
        app.state.http_client = httpx.AsyncClient(timeout=5.0)

    @app.on_event("shutdown")
    async def shutdown_http_client():
        await app.state.http_client.aclose()
