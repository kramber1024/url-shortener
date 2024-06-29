from fastapi import APIRouter, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.config import settings

templates: Jinja2Templates = Jinja2Templates(directory="frontend")
router: APIRouter = APIRouter(include_in_schema=False)


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "templates/signup.html",
        {
            "request": request,
            "brand_name": settings.app.NAME,
        },
    )


@router.get("/login", response_class=HTMLResponse)
async def signin(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "templates/signin.html",
        {
            "request": request,
            "brand_name": settings.app.NAME,
        },
    )

# TODO(kramber): Disable /api/docs when in production
# as well as /openapi.json
# 000
@router.get("/api/docs")
async def swagger() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.app.NAME + " - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

# TODO(kramber): Disable /api/redoc when in production
# 000
@router.get("/api/redoc")
async def redoc() -> HTMLResponse:
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=settings.app.NAME + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )
