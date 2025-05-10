import httpx
import logging

from fastapi import status, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from core.config import settings
from core.security import verify_access_token

logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

class AuthProxyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service_urls: dict[str, str], auth_prefix: str = '/auth'):
        super().__init__(app)
        self.service_urls = service_urls
        self.auth_prefix = auth_prefix

    @staticmethod
    def get_401_headers(request: Request) -> dict[str, str]:
        return {
            'WWW-Authenticate': 'Bearer',
            'Access-Control-Allow-Origin': request.headers.get('origin', ''),
            'Access-Control-Allow-Credentials': 'true',
        }

    async def _authenticate(self, request: Request) -> str | Response:
        # extract token from header or cookie
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                scheme, token = auth_header.split(' ')
            except ValueError:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={'error': 'Invalid authorization header format'},
                    headers=self.get_401_headers(request),
                )
            if scheme.lower() != 'bearer':
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={'error': f'Invalid auth scheme, must be Bearer, found {scheme}'},
                    headers=self.get_401_headers(request),
                )
        else:
            token = request.cookies.get(settings.cookie_name)

        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'error': 'Missing auth token'},
                headers=self.get_401_headers(request),
            )

        try:
            payload = verify_access_token(token)
        except Exception as e:
            logger.error(f'Token verification failed: {e}')
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'error': 'Invalid or expired token'},
                headers=self.get_401_headers(request),
            )

        user_id = payload.get('sub')
        if not user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'error': 'Malformed token payload'},
                headers=self.get_401_headers(request),
            )

        return user_id

    async def _proxy_request(self, request: Request, user_id: str | None) -> Response:
        path = request.url.path
        for prefix, base_url in self.service_urls.items():
            if path.startswith(f'/{prefix}'):
                # build downstream URL
                downstream_url = f'{base_url}{path}'
                if request.url.query:
                    downstream_url += f'?{request.url.query}'

                try:
                    async with httpx.AsyncClient() as client:
                        headers = dict(request.headers)
                        headers.pop('host', None)
                        if user_id:
                            headers['X-User-Id'] = user_id

                        resp = await client.request(
                            method=request.method,
                            url=downstream_url,
                            headers=headers,
                            content=await request.body(),
                            timeout=10.0,
                        )
                except httpx.RequestError as e:
                    logger.error(f'Downstream request failed: {e}')
                    return JSONResponse(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        content={'error': 'Cannot reach downstream service'},
                    )

                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    headers=resp.headers,
                )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'error': f'No service for path {path}'},
        )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger.debug(f'Dispatching request to path: {request.url.path}')

        # allow health and metrics through
        if request.url.path in ('/health', '/metrics'):
            return await call_next(request)

        # authenticate for all non-auth paths
        user = None
        if not request.url.path.startswith(self.auth_prefix):
            auth_result = await self._authenticate(request)
            if isinstance(auth_result, Response):
                return auth_result
            user = auth_result

        # proxy the request
        return await self._proxy_request(request, user)
