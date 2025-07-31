from fastapi import FastAPI, Depends,Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from .database import init_db, get_db
from . import crud_items, crud_tags, crud_item_tags
from .models import Item, ItemCreate, ItemUpdate, Tag, TagCreate, TagUpdate

# 初始化数据库
init_db()

app = FastAPI(
    title="LifeNote API",
    description="一个简单的笔记和标签管理API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to LifeNote API"}

# Items 路由
@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate, conn: sqlite3.Connection = Depends(get_db)):
    return crud_items.create_item(item, conn)

@app.get("/items/", response_model=list[Item])
async def get_all_items(conn: sqlite3.Connection = Depends(get_db)):
    return crud_items.get_all_items(conn)

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return crud_items.get_item(item_id, conn)

@app.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int, 
    item_update: ItemUpdate, 
    conn: sqlite3.Connection = Depends(get_db)
):
    return crud_items.update_item(item_id, item_update, conn)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return crud_items.delete_item(item_id, conn)

# Tags 路由
@app.post("/tags/", response_model=Tag)
async def create_tag(tag: TagCreate, conn: sqlite3.Connection = Depends(get_db)):
    return crud_tags.create_tag(tag, conn)

@app.get("/tags/", response_model=list[Tag])
async def get_all_tags(conn: sqlite3.Connection = Depends(get_db)):
    return crud_tags.get_all_tags(conn)

@app.get("/tags/{tag_id}", response_model=Tag)
async def get_tag(tag_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return crud_tags.get_tag(tag_id, conn)

@app.put("/tags/{tag_id}", response_model=Tag)
async def update_tag(
    tag_id: int, 
    tag_update: TagUpdate,  # 简单起见，直接接收name参数
    conn: sqlite3.Connection = Depends(get_db)
):
    return crud_tags.update_tag(tag_id, tag_update, conn)

@app.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return crud_tags.delete_tag(tag_id, conn)


# 在现有路由后添加

@app.get("/items/{item_id}/tags", response_model=list[Tag])
async def get_tags_by_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    return crud_item_tags.get_item_tags(item_id, conn)

@app.post("/items/{item_id}/tags/{tag_id}")
async def add_item_tag(
    item_id: int, 
    tag_id: int, 
    conn: sqlite3.Connection = Depends(get_db)
):
    crud_item_tags.add_tag_to_item(item_id, tag_id, conn)
    return {"message": "Tag added to item"}

@app.delete("/items/{item_id}/tags/{tag_id}")
async def remove_item_tag(
    item_id: int, 
    tag_id: int, 
    conn: sqlite3.Connection = Depends(get_db)
):
    crud_item_tags.remove_tag_from_item(item_id, tag_id, conn)
    return {"message": "Tag removed from item"}

@app.get("/tags/{tag_id}/items", response_model=list[Item])
async def get_items_with_tags(
    tag_id: int,
    conn: sqlite3.Connection = Depends(get_db)
):
    return crud_item_tags.get_items_by_tag(tag_id, conn)


@app.put("/items/{item_id}/tags")
async def replace_item_tags_endpoint(
    item_id: int,
    tag_ids: list[int],
    conn: sqlite3.Connection = Depends(get_db)
):
    crud_item_tags.replace_item_tags(item_id, tag_ids, conn)
    return {"message": "Tags replaced successfully"}