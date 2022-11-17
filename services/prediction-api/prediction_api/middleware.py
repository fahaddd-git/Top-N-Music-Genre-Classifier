from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, Request, RequestResponseEndpoint, Response
from starlette.types import ASGIApp


class LimitUploadFilesizeMiddleware(BaseHTTPMiddleware):
    """Middleware limiting ``POST`` request size to ``max_megabytes``"""

    # class implementation follows the formatting required by Starlette
    # see: https://www.starlette.io/middleware/#basehttpmiddleware

    def __init__(self, app: ASGIApp, max_megabytes: int):
        super().__init__(app)
        self._max_megabytes = max_megabytes
        self._missing_header_response = JSONResponse(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            content={"detail": "Missing content-length header."},
        )
        self._entity_too_large_response = JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"detail": "Content too large."},
        )

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Reject requests in excess of ``max_megabytes``"""
        # Inspired by:
        #   URL: https://github.com/tiangolo/fastapi/issues/362
        #   Date: 11/16/22
        if request.method.upper() == "POST":
            if (content_length := request.headers.get("content-length")) in {"", None}:
                return self._missing_header_response
            if int(content_length) > self._max_megabytes * 1024 * 1024:
                return self._entity_too_large_response
        return await call_next(request)
