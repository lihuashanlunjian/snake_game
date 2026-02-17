"""
@file    __init__.py
@brief   数据库模块初始化
@details 导出数据库相关类和函数
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

from .db_config import db, init_db
from .models import User, PasswordResetToken
from .user_dao import UserDAO

__all__ = ['db', 'init_db', 'User', 'PasswordResetToken', 'UserDAO']
