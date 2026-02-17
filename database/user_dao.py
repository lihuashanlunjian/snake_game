"""
@file    user_dao.py
@brief   用户数据访问对象
@details 实现用户信息的CRUD操作，提供数据访问层接口
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .db_config import db
from .models import User, PasswordResetToken

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserDAO:
    """
    @brief  用户数据访问对象
    @details 提供用户信息的增删改查操作
    """
    
    @staticmethod
    def create_user(username, email, password_hash):
        """
        @brief  创建新用户
        @param  username: 用户名
        @param  email: 邮箱地址
        @param  password_hash: 哈希后的密码
        @retval User: 创建的用户对象，失败返回None
        """
        try:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"用户创建成功: {username}")
            return user
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"用户创建失败（数据完整性错误）: {str(e)}")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"用户创建失败（数据库错误）: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        @brief  通过用户ID获取用户
        @param  user_id: 用户ID
        @retval User: 用户对象，不存在返回None
        """
        try:
            user = User.query.filter_by(user_id=user_id, is_active=True).first()
            return user
        except SQLAlchemyError as e:
            logger.error(f"查询用户失败（ID: {user_id}）: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_username(username):
        """
        @brief  通过用户名获取用户
        @param  username: 用户名
        @retval User: 用户对象，不存在返回None
        """
        try:
            user = User.query.filter_by(username=username, is_active=True).first()
            return user
        except SQLAlchemyError as e:
            logger.error(f"查询用户失败（用户名: {username}）: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        @brief  通过邮箱获取用户
        @param  email: 邮箱地址
        @retval User: 用户对象，不存在返回None
        """
        try:
            user = User.query.filter_by(email=email, is_active=True).first()
            return user
        except SQLAlchemyError as e:
            logger.error(f"查询用户失败（邮箱: {email}）: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_username_or_email(identifier):
        """
        @brief  通过用户名或邮箱获取用户
        @param  identifier: 用户名或邮箱
        @retval User: 用户对象，不存在返回None
        """
        user = UserDAO.get_user_by_username(identifier)
        if not user:
            user = UserDAO.get_user_by_email(identifier)
        return user
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        @brief  更新用户信息
        @param  user_id: 用户ID
        @param  kwargs: 要更新的字段和值
        @retval bool: 更新是否成功
        """
        try:
            user = UserDAO.get_user_by_id(user_id)
            if not user:
                logger.warning(f"用户不存在（ID: {user_id}）")
                return False
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            db.session.commit()
            logger.info(f"用户信息更新成功（ID: {user_id}）")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"用户信息更新失败（ID: {user_id}）: {str(e)}")
            return False
    
    @staticmethod
    def delete_user(user_id):
        """
        @brief  删除用户（软删除）
        @param  user_id: 用户ID
        @retval bool: 删除是否成功
        """
        try:
            user = UserDAO.get_user_by_id(user_id)
            if not user:
                logger.warning(f"用户不存在（ID: {user_id}）")
                return False
            
            user.is_active = False
            db.session.commit()
            logger.info(f"用户删除成功（ID: {user_id}）")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"用户删除失败（ID: {user_id}）: {str(e)}")
            return False
    
    @staticmethod
    def update_last_login(user_id):
        """
        @brief  更新最后登录时间
        @param  user_id: 用户ID
        @retval bool: 更新是否成功
        """
        return UserDAO.update_user(user_id, last_login_at=datetime.utcnow())
    
    @staticmethod
    def record_login_attempt(user_id, success):
        """
        @brief  记录登录尝试
        @param  user_id: 用户ID
        @param  success: 是否成功
        @retval bool: 记录是否成功
        """
        try:
            user = UserDAO.get_user_by_id(user_id)
            if not user:
                return False
            
            if success:
                user.login_attempt_count = 0
                user.last_login_attempt_at = None
                user.is_locked = False
                user.locked_until = None
            else:
                user.login_attempt_count += 1
                user.last_login_attempt_at = datetime.utcnow()
            
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"记录登录尝试失败（ID: {user_id}）: {str(e)}")
            return False
    
    @staticmethod
    def check_user_locked(user_id, max_attempts=5, lockout_duration_minutes=15):
        """
        @brief  检查用户是否被锁定
        @param  user_id: 用户ID
        @param  max_attempts: 最大尝试次数
        @param  lockout_duration_minutes: 锁定时长（分钟）
        @retval dict: 包含锁定状态和剩余时间的字典
        """
        try:
            user = UserDAO.get_user_by_id(user_id)
            if not user:
                return {'locked': False, 'remaining_time': 0}
            
            if user.is_locked and user.locked_until:
                if datetime.utcnow() < user.locked_until:
                    remaining = (user.locked_until - datetime.utcnow()).total_seconds()
                    return {'locked': True, 'remaining_time': int(remaining)}
                else:
                    user.is_locked = False
                    user.locked_until = None
                    user.login_attempt_count = 0
                    db.session.commit()
            
            if user.login_attempt_count >= max_attempts and user.last_login_attempt_at:
                lockout_until = user.last_login_attempt_at + timedelta(minutes=lockout_duration_minutes)
                
                if datetime.utcnow() < lockout_until:
                    user.is_locked = True
                    user.locked_until = lockout_until
                    db.session.commit()
                    remaining = (lockout_until - datetime.utcnow()).total_seconds()
                    return {'locked': True, 'remaining_time': int(remaining)}
                else:
                    user.login_attempt_count = 0
                    user.last_login_attempt_at = None
                    db.session.commit()
            
            return {'locked': False, 'remaining_time': 0}
        except SQLAlchemyError as e:
            logger.error(f"检查用户锁定状态失败（ID: {user_id}）: {str(e)}")
            return {'locked': False, 'remaining_time': 0}
    
    @staticmethod
    def lock_user(user_id, lockout_duration_minutes=15):
        """
        @brief  锁定用户
        @param  user_id: 用户ID
        @param  lockout_duration_minutes: 锁定时长（分钟）
        @retval bool: 锁定是否成功
        """
        locked_until = datetime.utcnow() + timedelta(minutes=lockout_duration_minutes)
        return UserDAO.update_user(user_id, is_locked=True, locked_until=locked_until)
    
    @staticmethod
    def unlock_user(user_id):
        """
        @brief  解锁用户
        @param  user_id: 用户ID
        @retval bool: 解锁是否成功
        """
        return UserDAO.update_user(
            user_id,
            is_locked=False,
            locked_until=None,
            login_attempt_count=0,
            last_login_attempt_at=None
        )


class PasswordResetTokenDAO:
    """
    @brief  密码重置令牌数据访问对象
    @details 提供令牌的创建、查询和删除操作
    """
    
    @staticmethod
    def create_token(user_id, token, expires_hours=1):
        """
        @brief  创建密码重置令牌
        @param  user_id: 用户ID
        @param  token: 令牌字符串
        @param  expires_hours: 过期时长（小时）
        @retval PasswordResetToken: 创建的令牌对象，失败返回None
        """
        try:
            expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
            reset_token = PasswordResetToken(
                token=token,
                user_id=user_id,
                expires_at=expires_at
            )
            db.session.add(reset_token)
            db.session.commit()
            logger.info(f"密码重置令牌创建成功（用户ID: {user_id}）")
            return reset_token
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"密码重置令牌创建失败: {str(e)}")
            return None
    
    @staticmethod
    def get_token_by_token_string(token_string):
        """
        @brief  通过令牌字符串获取令牌
        @param  token_string: 令牌字符串
        @retval PasswordResetToken: 令牌对象，不存在返回None
        """
        try:
            token = PasswordResetToken.query.filter_by(token=token_string, is_used=False).first()
            return token
        except SQLAlchemyError as e:
            logger.error(f"查询令牌失败: {str(e)}")
            return None
    
    @staticmethod
    def mark_token_as_used(token_id):
        """
        @brief  标记令牌为已使用
        @param  token_id: 令牌ID
        @retval bool: 标记是否成功
        """
        try:
            token = PasswordResetToken.query.get(token_id)
            if token:
                token.is_used = True
                db.session.commit()
                logger.info(f"令牌已标记为使用（ID: {token_id}）")
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"标记令牌失败（ID: {token_id}）: {str(e)}")
            return False
    
    @staticmethod
    def delete_expired_tokens():
        """
        @brief  删除过期的令牌
        @retval int: 删除的令牌数量
        """
        try:
            expired_tokens = PasswordResetToken.query.filter(
                PasswordResetToken.expires_at < datetime.utcnow()
            ).all()
            
            count = len(expired_tokens)
            for token in expired_tokens:
                db.session.delete(token)
            
            db.session.commit()
            logger.info(f"删除过期令牌: {count}个")
            return count
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"删除过期令牌失败: {str(e)}")
            return 0
    
    @staticmethod
    def delete_user_tokens(user_id):
        """
        @brief  删除用户的所有令牌
        @param  user_id: 用户ID
        @retval int: 删除的令牌数量
        """
        try:
            tokens = PasswordResetToken.query.filter_by(user_id=user_id).all()
            count = len(tokens)
            for token in tokens:
                db.session.delete(token)
            db.session.commit()
            logger.info(f"删除用户令牌（用户ID: {user_id}）: {count}个")
            return count
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"删除用户令牌失败（用户ID: {user_id}）: {str(e)}")
            return 0
