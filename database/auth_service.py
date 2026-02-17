"""
@file    auth_service.py
@brief   用户认证服务
@details 实现用户注册、登录、密码重置等业务逻辑，使用数据库存储
@author  AI Assistant
@date    2026-02-17
@version V1.0.1
"""

import secrets
import hashlib
import logging
from datetime import datetime
from functools import wraps
from flask import request, jsonify, session
from .user_dao import UserDAO, PasswordResetTokenDAO
from .validators import UserValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


class AuthService:
    """
    @brief  用户认证服务类
    @details 提供用户注册、登录、密码管理等功能
    """
    
    @staticmethod
    def hash_password(password):
        """
        @brief  对密码进行哈希处理
        @param  password: 明文密码
        @retval str: 哈希后的密码字符串
        """
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}${hash_obj.hexdigest()}"
    
    @staticmethod
    def verify_password(password, hashed_password):
        """
        @brief  验证密码是否正确
        @param  password: 明文密码
        @param  hashed_password: 哈希后的密码
        @retval bool: 密码是否匹配
        """
        try:
            salt, hash_value = hashed_password.split('$')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except ValueError:
            logger.error("密码哈希格式错误")
            return False
    
    @staticmethod
    def register_user(username, email, password):
        """
        @brief  注册新用户
        @param  username: 用户名
        @param  email: 邮箱地址
        @param  password: 密码
        @retval dict: 包含状态和消息的字典
        """
        validation_result = UserValidator.validate_registration_data(username, email, password)
        if not validation_result['valid']:
            return {'success': False, 'message': validation_result['message']}
        
        username = UserValidator.sanitize_input(username)
        email = UserValidator.sanitize_input(email).lower()
        
        existing_user = UserDAO.get_user_by_username(username)
        if existing_user:
            logger.warning(f"注册失败：用户名已存在 - {username}")
            return {'success': False, 'message': '用户名已存在'}
        
        existing_email = UserDAO.get_user_by_email(email)
        if existing_email:
            logger.warning(f"注册失败：邮箱已被注册 - {email}")
            return {'success': False, 'message': '邮箱已被注册'}
        
        password_hash = AuthService.hash_password(password)
        
        user = UserDAO.create_user(username, email, password_hash)
        
        if user:
            logger.info(f"用户注册成功: {username}")
            return {'success': True, 'message': '注册成功', 'user_id': user.user_id}
        else:
            logger.error(f"用户注册失败: {username}")
            return {'success': False, 'message': '注册失败，请稍后重试'}
    
    @staticmethod
    def login_user(identifier, password):
        """
        @brief  用户登录
        @param  identifier: 用户名或邮箱
        @param  password: 密码
        @retval dict: 包含状态和消息的字典
        """
        validation_result = UserValidator.validate_login_data(identifier, password)
        if not validation_result['valid']:
            return {'success': False, 'message': validation_result['message']}
        
        identifier = UserValidator.sanitize_input(identifier)
        
        user = UserDAO.get_user_by_username_or_email(identifier)
        
        if not user:
            logger.warning(f"登录失败：用户不存在 - {identifier}")
            return {'success': False, 'message': '用户名或密码错误'}
        
        lockout_status = UserDAO.check_user_locked(
            user.user_id,
            MAX_LOGIN_ATTEMPTS,
            LOCKOUT_DURATION_MINUTES
        )
        
        if lockout_status['locked']:
            logger.warning(f"登录失败：账户已锁定 - {user.username}")
            return {
                'success': False,
                'message': f"账户已锁定，请{lockout_status['remaining_time']}秒后重试",
                'locked': True,
                'remaining_time': lockout_status['remaining_time']
            }
        
        if not AuthService.verify_password(password, user.password_hash):
            UserDAO.record_login_attempt(user.user_id, False)
            logger.warning(f"登录失败：密码错误 - {user.username}")
            return {'success': False, 'message': '用户名或密码错误'}
        
        UserDAO.record_login_attempt(user.user_id, True)
        UserDAO.update_last_login(user.user_id)
        
        logger.info(f"用户登录成功: {user.username}")
        return {
            'success': True,
            'message': '登录成功',
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email
        }
    
    @staticmethod
    def create_reset_token(email):
        """
        @brief  创建密码重置令牌
        @param  email: 邮箱地址
        @retval dict: 包含状态和令牌的字典
        """
        email = UserValidator.sanitize_input(email).lower()
        
        email_validation = UserValidator.validate_email(email)
        if not email_validation['valid']:
            return {'success': False, 'message': email_validation['message']}
        
        user = UserDAO.get_user_by_email(email)
        
        if not user:
            logger.warning(f"密码重置失败：邮箱未注册 - {email}")
            return {'success': False, 'message': '该邮箱未注册'}
        
        token = secrets.token_urlsafe(32)
        
        reset_token = PasswordResetTokenDAO.create_token(user.user_id, token, expires_hours=1)
        
        if reset_token:
            logger.info(f"密码重置令牌创建成功: {email}")
            return {
                'success': True,
                'message': '重置密码链接已发送',
                'token': token
            }
        else:
            logger.error(f"密码重置令牌创建失败: {email}")
            return {'success': False, 'message': '创建重置令牌失败'}
    
    @staticmethod
    def reset_password(token, new_password):
        """
        @brief  重置密码
        @param  token: 重置令牌
        @param  new_password: 新密码
        @retval dict: 包含状态和消息的字典
        """
        password_validation = UserValidator.validate_password(new_password)
        if not password_validation['valid']:
            return {'success': False, 'message': password_validation['message']}
        
        reset_token = PasswordResetTokenDAO.get_token_by_token_string(token)
        
        if not reset_token:
            logger.warning("密码重置失败：无效的令牌")
            return {'success': False, 'message': '无效的重置链接'}
        
        if datetime.utcnow() > reset_token.expires_at:
            PasswordResetTokenDAO.mark_token_as_used(reset_token.token_id)
            logger.warning("密码重置失败：令牌已过期")
            return {'success': False, 'message': '重置链接已过期'}
        
        user = UserDAO.get_user_by_id(reset_token.user_id)
        if not user:
            logger.error(f"密码重置失败：用户不存在 - {reset_token.user_id}")
            return {'success': False, 'message': '用户不存在'}
        
        password_hash = AuthService.hash_password(new_password)
        
        update_success = UserDAO.update_user(user.user_id, password_hash=password_hash)
        
        if update_success:
            PasswordResetTokenDAO.mark_token_as_used(reset_token.token_id)
            UserDAO.unlock_user(user.user_id)
            logger.info(f"密码重置成功: {user.username}")
            return {'success': True, 'message': '密码重置成功'}
        else:
            logger.error(f"密码重置失败: {user.username}")
            return {'success': False, 'message': '密码重置失败'}
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        @brief  修改密码
        @param  user_id: 用户ID
        @param  old_password: 旧密码
        @param  new_password: 新密码
        @retval dict: 包含状态和消息的字典
        """
        password_validation = UserValidator.validate_password(new_password)
        if not password_validation['valid']:
            return {'success': False, 'message': password_validation['message']}
        
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'message': '用户不存在'}
        
        if not AuthService.verify_password(old_password, user.password_hash):
            logger.warning(f"修改密码失败：旧密码错误 - {user.username}")
            return {'success': False, 'message': '旧密码错误'}
        
        password_hash = AuthService.hash_password(new_password)
        
        update_success = UserDAO.update_user(user.user_id, password_hash=password_hash)
        
        if update_success:
            logger.info(f"密码修改成功: {user.username}")
            return {'success': True, 'message': '密码修改成功'}
        else:
            logger.error(f"密码修改失败: {user.username}")
            return {'success': False, 'message': '密码修改失败'}
    
    @staticmethod
    def get_user_info(user_id):
        """
        @brief  获取用户信息
        @param  user_id: 用户ID
        @retval dict: 包含用户信息的字典
        """
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'message': '用户不存在'}
        
        return {
            'success': True,
            'user': user.to_dict()
        }


def login_required(f):
    """
    @brief  登录验证装饰器
    @details 检查用户是否已登录，未登录则返回错误或重定向
    @param  f: 被装饰的函数
    @retval function: 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({
                    'success': False,
                    'message': '请先登录后再开始游戏',
                    'need_login': True
                }), 401
            from flask import redirect, url_for
            return redirect(url_for('login_page', message='请先登录后再开始游戏'))
        return f(*args, **kwargs)
    return decorated_function
