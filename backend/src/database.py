from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "lifeNote.db"

# 自动创建数据目录
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    """初始化数据库和所有表"""
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()
        
        # 检查并创建 items 表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
        
        # 检查并创建 tags 表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tags'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

        # 创建关联表
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='item_tags'
        """)
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE item_tags (
                    item_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    PRIMARY KEY (item_id, tag_id),
                    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
                )
            """)
            cursor.execute("CREATE INDEX idx_item_tags_item ON item_tags(item_id)")
            cursor.execute("CREATE INDEX idx_item_tags_tag ON item_tags(tag_id)")
        
        conn.commit()

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

