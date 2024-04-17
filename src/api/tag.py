from typing import List
from fastapi import APIRouter, Depends
from api.dependencies import current_user, tag_service_dependency
from models.users import User
from schemas.tag import TagBase


router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("", response_model=List[TagBase])
async def get_tags(
    service: tag_service_dependency,
    current_user: User = Depends(current_user)
):
    tags = await service.get_tags(current_user.id)
    return tags


@router.post("", response_model=TagBase)
async def create_tag(
    request: TagBase,
    service: tag_service_dependency,
    current_user: User = Depends(current_user),
):
    new_tag = await service.create_tag(request, current_user.id)
    return new_tag


@router.post("/set", status_code=201)
async def set_tags(
    task_id: int,
    tag_id: int, 
    service: tag_service_dependency,
    current_user: User = Depends(current_user),
):
    await service.set_tags(task_id, tag_id)
    