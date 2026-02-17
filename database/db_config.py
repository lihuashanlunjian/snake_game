"""
@file    db_config.py
@brief   数据库配置和连接管理
@details 配置SQLite数据库连接，提供数据库初始化功能
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import os
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(app):
    """
    @brief  初始化数据库连接
    @param  app: Flask应用实例
    @retval None
    """
    database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snake_game.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"数据库表创建失败: {str(e)}")
            raise
