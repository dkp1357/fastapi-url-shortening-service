from fastapi import APIRouter
from sqlmodel import Session, select

router = APIRouter()

import random
import string
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, Response

from app import crud
from app.database import get_session
from app.models import *


# default length of 6
def generate_short_code(length: Optional[int]):
    characters = string.ascii_letters + string.digits
    short_code = ""

    if length is None:
        length = 6

    for _ in range(length):
        short_code += random.choice(characters)

    return short_code


def create_URLResponse(entry: URL) -> URLResponse:
    response = URLResponse(
        id=entry.id,
        url=entry.url,
        short_code=entry.short_code,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        access_count=entry.access_count,
    )
    return response


@router.post("/shorten", response_model=URLResponse, status_code=201)
async def create_short_url(
    request: URLRequest, session: Session = Depends(get_session)
):
    # check if url exists
    for row in session.exec(select(URL)).all():
        if row.url == request.url:
            return create_URLResponse(row)

    short_code = generate_short_code(request.length)
    # ensure uniqueness
    while crud.get_short_url(session, short_code) is not None:
        short_code = generate_short_code(request.length)

    return create_URLResponse(crud.create_short_url(session, request.url, short_code))


@router.get("/shorten/{short_code}", response_model=URLResponse, status_code=200)
async def get_short_url(short_code: str, session: Session = Depends(get_session)):
    entry = crud.get_short_url(session, short_code)

    if entry is None:
        raise HTTPException(status_code=404, detail="short_code not found")

    crud.increment_access_count(session, short_code)

    return create_URLResponse(entry)


@router.put("/shorten/{short_code}", response_model=URLResponse, status_code=200)
def update_short_url(
    short_code: str, request: URLRequest, session: Session = Depends(get_session)
):
    entry = crud.update_short_url(
        session=session, url=request.url, short_code=short_code
    )

    if entry is None:
        raise HTTPException(status_code=404, detail="short_code not found")

    return create_URLResponse(entry)


@router.delete("/shorten/{short_code}", status_code=204)
def delete_short_url(short_code: str, session: Session = Depends(get_session)):
    entry = crud.get_short_url(session, short_code)

    if entry is None:
        raise HTTPException(status_code=404, detail="short_code not found")

    crud.delete_short_url(session, short_code)
    return Response(status_code=204)
