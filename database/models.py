"""
@file    models.py
@brief   数据库模型定义
@details 定义用户信息表和密码重置令牌表的数据结构
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

from datetime import datetime
from .db_config import db


class User(db.Model):
    """
    @brief  用户信息表模型
    @details 存储用户的基本信息和登录状态
    """
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)
    login_attempt_count = db.Column(db.Integer, default=0)
    last_login_attempt_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_locked = db.Column(db.Boolean, default=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    reset_tokens = db.relationship('PasswordResetToken', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """
        @brief  将用户对象转换为字典
        @retval dict: 用户信息字典
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'is_active': self.is_active,
            'is_locked': self.is_locked
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class PasswordResetToken(db.Model):
    """
    @brief  密码重置令牌表模型
    @details 存储密码重置令牌及其有效期
    """
    __tablename__ = 'password_reset_tokens'
    
    token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """
        @brief  将令牌对象转换为字典
        @retval dict: 令牌信息字典
        """
        return {
            'token_id': self.token_id,
            'token': self.token,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_used': self.is_used
        }
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token[:10]}...>'
