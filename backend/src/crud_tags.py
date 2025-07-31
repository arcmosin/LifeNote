from .database import get_db
from .models import Tag, TagCreate, TagUpdate
from fastapi import HTTPException
import sqlite3
from datetime import datetime

def create_tag(tag: TagCreate, conn: sqlite3.Connection):
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO tags (name, created_at, updated_at) VALUES (?,?,?)",
            (tag.name,time_now,time_now)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Tag name already exists")
    
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM tags WHERE id = ?", (new_id,))
    return dict(cursor.fetchone())

def get_tag(tag_id: int, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags WHERE id = ?", (tag_id,))
    tag = cursor.fetchone()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return dict(tag)

def get_all_tags(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags ORDER BY created_at DESC")
    return [dict(tag) for tag in cursor.fetchall()]

def update_tag(tag_id: int, tag_update: TagUpdate, conn: sqlite3.Connection):
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM tags WHERE id = ?", (tag_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Tag not found")
    
    if not tag_update.name or not tag_update.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Tag name cannot be empty"
        )
    
    
    try:
        cursor.execute(
            "UPDATE tags SET name = ?, updated_at = ? WHERE id = ?",
            (tag_update.name,time_now, tag_id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Tag name already exists")
    
    cursor.execute("SELECT * FROM tags WHERE id = ?", (tag_id,))
    return dict(cursor.fetchone())

def delete_tag(tag_id: int, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags WHERE id = ?", (tag_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Tag not found")
    
    cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    conn.commit()
    return {"message": "Tag deleted"}