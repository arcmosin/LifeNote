# src/__init__.py

# 可选：显式导出公共API
__all__ = ['main', 'database', 'models', 'crud_items', 'crud_tags','crud_item_tags']

# 可选：包版本信息
__version__ = '0.1.0'

# 可选：初始化代码
from .database import init_db

# 自动初始化数据库（谨慎使用，可能更适合在main.py中显式调用）
# init_db()