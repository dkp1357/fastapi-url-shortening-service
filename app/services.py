import random
import string
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from fastapi import HTTPException, Response

from app.models import URLRequest, URLResponse
from app.routes import router, url_store


# default length of 6
def generate_short_code(length: Optional[int]):
    characters = string.ascii_letters + string.digits
    short_code = ""

    if length is None:
        length = 6

    for _ in range(length):
        short_code += random.choice(characters)

    return short_code


@router.post("/shorten", response_model=URLResponse, status_code=201)
async def shorten_url(request: URLRequest):
    # check if url exists in memory
    for key in url_store:
        if url_store[key].url == request.url:
            return url_store[key]

    short_code = generate_short_code(request.length)

    # to get unique short_code
    while short_code in url_store:
        short_code = generate_short_code(request.length)

    url_store[short_code] = URLResponse(
        id=len(url_store) + 1,
        url=request.url,
        shortCode=short_code,
        createdAt=datetime.now(tz=ZoneInfo("Asia/Kolkata")),
        updatedAt=datetime.now(tz=ZoneInfo("Asia/Kolkata")),
        accessCount=0,
    )

    return url_store[short_code]


@router.get("/shorten/{short_code}", response_model=URLResponse, status_code=200)
async def get_original_url(short_code: str):
    if short_code not in url_store:
        raise HTTPException(status_code=404, detail="shortCode not found")

    url_store[short_code].accessCount += 1
    return url_store[short_code]


@router.put("/shorten/{short_code}", response_model=URLResponse, status_code=200)
async def update_short_url(short_code: str, request: URLRequest):
    if short_code not in url_store:
        raise HTTPException(status_code=404, detail="shortCode not found")

    entry = url_store[short_code]
    entry.url = request.url
    entry.updatedAt = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

    url_store[short_code] = entry

    return url_store[short_code]


@router.delete("/shorten/{short_code}", status_code=204)
async def delete_short_url(short_code: str):
    if short_code not in url_store:
        raise HTTPException(status_code=404, detail="shortCode not found")

    del url_store[short_code]
    return Response(status_code=204)


@router.get("/shorten/{short_code}/stats", response_model=URLResponse)
async def get_url_stats(short_code: str):
    if short_code not in url_store:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return url_store[short_code]
