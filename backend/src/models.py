from pydantic import BaseModel
from typing import Optional

#-------------------------------------------------

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

class TagIDs(BaseModel):
    tag_ids: list[int]

class TagUpdate(BaseModel):
    name: str
#-------------------------------------------------

class ItemBase(BaseModel):
    title: str
    content: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Item(ItemBase):
    id: int
    created_at: str
    updated_at: str
    tags: list[Tag] = []  # 添加标签列表字段

    class Config:
      orm_mode = True


