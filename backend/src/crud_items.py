from datetime import datetime
from .database import get_db
from .models import Item, ItemCreate, ItemUpdate
from fastapi import HTTPException, Depends
import sqlite3

# crud_items.py
from .crud_item_tags import get_item_tags

def create_item(item: ItemCreate, conn: sqlite3.Connection):
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        "INSERT INTO items (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (item.title, item.content, time_now, time_now)
    )
    conn.commit()
    
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM items WHERE id = ?", (new_id,))
    return dict(cursor.fetchone())

def get_item(item_id: int, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_dict = dict(item)
    item_dict['tags'] = get_item_tags(item_id, conn)
    return item_dict

def get_all_items(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items ORDER BY updated_at DESC")
    items = [dict(item) for item in cursor.fetchall()]
    
    # 为每个item添加tags
    for item in items:
        item['tags'] = get_item_tags(item['id'], conn)
    
    return items

def update_item(item_id: int, item_update: ItemUpdate, conn: sqlite3.Connection):
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Item not found")
    
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
    
    update_query = f"UPDATE items SET {', '.join(update_fields)} WHERE id = ?"
    params.append(item_id)
    
    cursor.execute(update_query, tuple(params))
    conn.commit()
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    return dict(cursor.fetchone())

def delete_item(item_id: int, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Item not found")
    
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted"}