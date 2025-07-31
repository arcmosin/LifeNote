# crud_item_tags.py
from fastapi import HTTPException
from .database import get_db
from typing import List
import sqlite3

def add_tag_to_item(item_id: int, tag_id: int, conn: sqlite3.Connection):
    """为笔记添加标签"""
    cursor = conn.cursor()
    
    # 检查项目和标签是否存在
    cursor.execute("SELECT 1 FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Item not found")
    
    cursor.execute("SELECT 1 FROM tags WHERE id = ?", (tag_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # 检查是否已存在关联
    cursor.execute("SELECT 1 FROM item_tags WHERE item_id = ? AND tag_id = ?", (item_id, tag_id))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Tag already assigned to item")
    
    cursor.execute(
        "INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)",
        (item_id, tag_id)
    )
    conn.commit()

def remove_tag_from_item(item_id: int, tag_id: int, conn: sqlite3.Connection):
    """从笔记移除标签"""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM item_tags WHERE item_id = ? AND tag_id = ?",
        (item_id, tag_id)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tag not assigned to item")
    conn.commit()

def get_item_tags(item_id: int, conn: sqlite3.Connection) -> List[dict]:
    """获取笔记的所有标签"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tags.id, tags.name , tags.created_at , tags.updated_at
        FROM tags
        JOIN item_tags ON tags.id = item_tags.tag_id
        WHERE item_tags.item_id = ?
    """, (item_id,))
    return [dict(row) for row in cursor.fetchall()]

def get_items_by_tag(tag_id: int, conn: sqlite3.Connection) -> List[dict]:
    """获取具有特定标签的所有笔记"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT items.* 
        FROM items
        JOIN item_tags ON items.id = item_tags.item_id
        WHERE item_tags.tag_id = ?
    """, (tag_id,))
    return [dict(row) for row in cursor.fetchall()]

def get_items_by_tags(tag_ids: List[int], conn: sqlite3.Connection) -> List[dict]:
    """获取同时具有所有指定标签的所有笔记"""
    if not tag_ids:
        return []
    
    cursor = conn.cursor()
    
    # 构建查询语句
    query = """
        SELECT i.* 
        FROM items i
        WHERE (
            SELECT COUNT(DISTINCT it.tag_id) 
            FROM item_tags it 
            WHERE it.item_id = i.id AND it.tag_id IN ({})
        ) = ?
    """.format(','.join(['?'] * len(tag_ids)))
    
    # 执行查询
    cursor.execute(query, (*tag_ids, len(tag_ids)))
    return [dict(row) for row in cursor.fetchall()]


from fastapi import HTTPException

def replace_item_tags(item_id: int, tag_ids: List[int], conn: sqlite3.Connection):
    """覆盖式更新笔记标签（全量替换）"""
    cursor = conn.cursor()
    # print("item_id,tag_ids",item_id,tag_ids)
    try:
        # 0. 启动事务（SQLite默认启用，显式声明更清晰）
        conn.execute("BEGIN TRANSACTION")
        
        # 1. 检查笔记是否存在
        cursor.execute("SELECT 1 FROM items WHERE id = ?", (item_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Item not found")
        
        # 2. 检查所有新标签是否存在（一次性查询）
        if tag_ids:  # 避免空列表的SQL语法错误
            cursor.execute(
                "SELECT id FROM tags WHERE id IN ({})".format(
                    ",".join("?" * len(tag_ids))
                ), tag_ids
            )
            existing_tags = {row[0] for row in cursor.fetchall()}
            missing_tags = set(tag_ids) - existing_tags
            if missing_tags:
                raise HTTPException(
                    status_code=404,
                    detail=f"Tags not found: {missing_tags}"
                )
        
        # 3. 删除所有旧关联
        cursor.execute(
            "DELETE FROM item_tags WHERE item_id = ?",
            (item_id,)
        )
        
        # 4. 批量插入新关联（如果tag_ids非空）
        if tag_ids:
            cursor.executemany(
                "INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)",
                [(item_id, tag_id) for tag_id in tag_ids]
            )
        
        conn.commit()
        return {"message": "Tags replaced successfully"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")