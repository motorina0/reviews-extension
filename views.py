import json

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists

from . import reviews_ext, reviews_renderer
from .crud import get_public_survey, get_public_survey_items

templates = Jinja2Templates(directory="templates")


@reviews_ext.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    return reviews_renderer().TemplateResponse(
        "reviews/index.html", {"request": request, "user": user.dict()}
    )

@reviews_ext.get("/survey/{survey_id}", response_class=HTMLResponse)
async def public_survey(survey_id: str,
    request: Request,
):
    public_survey = await get_public_survey(survey_id)
    survey_items = await get_public_survey_items(survey_id)
    public_items = [i.dict() for i in survey_items]

    return reviews_renderer().TemplateResponse(
        "reviews/survey.html", {"request": request, "survey": public_survey, "items": public_items}
    )
