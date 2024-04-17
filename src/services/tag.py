from typing import List
from repositories.tag import TagRepository
from schemas.tag import TagBase


class TagService:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = TagRepository


    async def create_tag(self, request: TagBase, user_id: int) -> TagBase:
        new_tag = await self.repository.create_tag(request, user_id)
        return new_tag 
    

    async def get_tags(self, user_id: int) -> List[TagBase]:
        tags = await self.repository.get_tags(user_id)
        return tags 
    

    async def set_tags(self, task_id, tag_id):
        await self.repository.set_tags(task_id=task_id, tag_id=tag_id)