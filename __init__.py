import asyncio

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_reviews")

reviews_ext: APIRouter = APIRouter(prefix="/reviews", tags=["reviews"])

reviews_static_files = [
    {
        "path": "/reviews/static",
        "app": StaticFiles(packages=[("lnbits", "extensions/reviews/static")]),
        "name": "reviews_static",
    }
]


def reviews_renderer():
    return template_renderer(["lnbits/extensions/reviews/templates"])


from .tasks import wait_for_paid_invoices
from .views import *
from .views_api import *


def tpos_start():
    loop = asyncio.get_event_loop()
    loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
