from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, models,  oauth2

router = APIRouter(
    tags=['Authentication']
)

