from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sqlite3

# 创建 FastAPI 实例
app = FastAPI(
    title="简单后端API",
    description="这是一个使用FastAPI搭建的简单后端",
    version="0.1.0"
)

# 添加 CORS 中间件以允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应更严格限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库连接函数
def get_db():
    conn = sqlite3.connect('lifeNote.db')
    conn.row_factory = sqlite3.Row  # 让结果以字典形式返回
    try:
        yield conn
    finally:
        conn.close()



# 初始化数据库（只需要运行一次）
# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # 检查表是否存在（可选）
#     cursor.execute("""
#         SELECT name FROM sqlite_master 
#         WHERE type='table' AND name='items'
#     """)
#     if not cursor.fetchone():
#         # 如果表不存在则创建
#         cursor.execute("""
#             CREATE TABLE items (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 title TEXT NOT NULL,
#                 content TEXT,
#                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                 updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         conn.commit()
#     conn.close()

# 在应用启动时检查数据库
# init_db()

# 定义数据模型
class Item(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class ItemCreate(BaseModel):
    title: str
    content: str

# 根路由
@app.get("/")
async def root():
    return {"message": "欢迎使用简单后端API"}

# 获取所有项目
@app.get("/items/",response_model=list[dict])
# async def get_all_items():
#     return fake_db
async def get_all_items(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return [dict(item) for item in items]  # 将Row对象转为字典



# 获取单个项目
# @app.get("/items/{item_id}")
# async def get_item(item_id: int):
#     item = next((c for c in fake_db if c["id"] == item_id), None)
#     if not item:
#         raise HTTPException(status_code=404, detail="笔记未找到")
#     return item
@app.get("/items/{item_id}",response_model=list[dict])
async def get_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="笔记未找到")
    return dict(item)

# 创建新项目
# @app.post("/items/")
# async def create_item(item: Item):
#     new_id = max(c["id"] for c in fake_db) + 1 if fake_db else 1
#     time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     new_item = {
#         "id": new_id,
#         "title": item.title,
#         "content": item.content,
#         "created_at": time_now,
#         "updated_at": time_now
#     }
#     fake_db.append(new_item)
#     return new_item
@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        """
        INSERT INTO items (title, content, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """,
        (item.title, item.content, time_now, time_now)
    )
    conn.commit()
    
    # 获取刚插入的记录的ID
    new_id = cursor.lastrowid
    
    # 返回新创建的记录
    cursor.execute("SELECT * FROM items WHERE id = ?", (new_id,))
    new_item = cursor.fetchone()
    
    return dict(new_item)


# 更新项目
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item_update: ItemUpdate):
#     item = next((c for c in fake_db if c["id"] == item_id), None)
#     time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     if not item:
#         raise HTTPException(status_code=404, detail="卡片未找到")
    
#     if item_update.title is not None:
#         item["title"] = item_update.title
#     if item_update.content is not None:
#         item["content"] = item_update.content

#     item["updated_at"] = time_now
    
#     return item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int, 
    item_update: ItemUpdate, 
    conn: sqlite3.Connection = Depends(get_db)
):
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 先检查项目是否存在
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="卡片未找到")
    
    # 构建更新语句
    update_fields = []
    params = []
    
    if item_update.title is not None:
        update_fields.append("title = ?")
        params.append(item_update.title)
    
    if item_update.content is not None:
        update_fields.append("content = ?")
        params.append(item_update.content)
    
    update_fields.append("updated_at = ?")
    params.append(time_now)
    
    # 执行更新
    update_query = f"""
    UPDATE items 
    SET {', '.join(update_fields)}
    WHERE id = ?
    """
    params.append(item_id)
    
    cursor.execute(update_query, tuple(params))
    conn.commit()
    
    # 返回更新后的记录
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    updated_item = cursor.fetchone()
    
    return dict(updated_item)

# 删除项目
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     # if item_id not in fake_db:
#     #     raise HTTPException(status_code=404, detail="项目未找到")
    
#     # deleted_item = fake_db.pop(item_id)
#     # return {"message": "项目已删除", "deleted_item": deleted_item}

#     global fake_db
#     item = next((c for c in fake_db if c["id"] == item_id), None)
#     if not item:
#         raise HTTPException(status_code=404, detail="卡片未找到")
    
#     fake_db = [c for c in fake_db if c["id"] != item_id]
#     return {"message": "卡片已删除", "deleted_item": item}
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    
    # 先检查项目是否存在
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="卡片未找到")
    
    # 执行删除
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    
    return {"message": "卡片删除成功"}