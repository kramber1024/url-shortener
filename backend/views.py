from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.configs import settings

templates: Jinja2Templates = Jinja2Templates(directory="frontend")
router: APIRouter = APIRouter(include_in_schema=False)


@router.get("/signup", response_class=HTMLResponse)
async def regsiter(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "templates/signup.html",
        {
            "request": request,
            "brand_name": settings.app.NAME,
        },
    )
