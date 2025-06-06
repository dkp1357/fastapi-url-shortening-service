from fastapi import APIRouter

router = APIRouter()

# in memory data for now
# key = short_code: str, value = URLResponse
url_store = {}

# base url
BASE_DOMAIN = "http://127.0.0.1:8000"

from app.services import *
