"""
@file    auth.py
@brief   用户认证模块
@details 实现用户注册、登录、密码重置等功能
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session


USERS_FILE = 'users.json'
RESET_TOKENS_FILE = 'reset_tokens.json'
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 15


def hash_password(password):
    """
    @brief  对密码进行哈希处理
    @param  password: 明文密码
    @retval 哈希后的密码字符串
    """
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"


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
        return False


def load_users():
    """
    @brief  加载用户数据
    @retval dict: 用户数据字典
    """
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_users(users):
    """
    @brief  保存用户数据
    @param  users: 用户数据字典
    @retval None
    """
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def load_reset_tokens():
    """
    @brief  加载密码重置令牌
    @retval dict: 重置令牌字典
    """
    if os.path.exists(RESET_TOKENS_FILE):
        with open(RESET_TOKENS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_reset_tokens(tokens):
    """
    @brief  保存密码重置令牌
    @param  tokens: 重置令牌字典
    @retval None
    """
    with open(RESET_TOKENS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)


def find_user_by_username_or_email(users, identifier):
    """
    @brief  通过用户名或邮箱查找用户
    @param  users: 用户数据字典
    @param  identifier: 用户名或邮箱
    @retval tuple: (用户名, 用户数据) 或 (None, None)
    """
    for username, user_data in users.items():
        if username == identifier or user_data.get('email') == identifier:
            return username, user_data
    return None, None


def check_login_attempts(users, username):
    """
    @brief  检查登录尝试次数
    @param  users: 用户数据字典
    @param  username: 用户名
    @retval dict: 包含是否锁定和剩余时间的字典
    """
    user = users.get(username)
    if not user:
        return {'locked': False, 'remaining_time': 0}
    
    login_attempts = user.get('login_attempts', {})
    attempts = login_attempts.get('count', 0)
    last_attempt = login_attempts.get('last_attempt')
    
    if attempts >= MAX_LOGIN_ATTEMPTS and last_attempt:
        last_time = datetime.fromisoformat(last_attempt)
        lockout_end = last_time + timedelta(minutes=LOCKOUT_DURATION)
        
        if datetime.now() < lockout_end:
            remaining = (lockout_end - datetime.now()).total_seconds()
            return {'locked': True, 'remaining_time': int(remaining)}
        else:
            user['login_attempts'] = {'count': 0, 'last_attempt': None}
            save_users(users)
    
    return {'locked': False, 'remaining_time': 0}


def record_login_attempt(users, username, success):
    """
    @brief  记录登录尝试
    @param  users: 用户数据字典
    @param  username: 用户名
    @param  success: 是否成功
    @retval None
    """
    if username not in users:
        return
    
    if success:
        users[username]['login_attempts'] = {'count': 0, 'last_attempt': None}
    else:
        attempts = users[username].get('login_attempts', {}).get('count', 0)
        users[username]['login_attempts'] = {
            'count': attempts + 1,
            'last_attempt': datetime.now().isoformat()
        }
    
    save_users(users)


def register_user(username, email, password):
    """
    @brief  注册新用户
    @param  username: 用户名
    @param  email: 邮箱地址
    @param  password: 密码
    @retval dict: 包含状态和消息的字典
    """
    users = load_users()
    
    if username in users:
        return {'success': False, 'message': '用户名已存在'}
    
    for user_data in users.values():
        if user_data.get('email') == email:
            return {'success': False, 'message': '邮箱已被注册'}
    
    if len(username) < 3:
        return {'success': False, 'message': '用户名至少需要3个字符'}
    
    if not username.isalnum() and '_' not in username:
        return {'success': False, 'message': '用户名只能包含字母、数字和下划线'}
    
    if len(password) < 6:
        return {'success': False, 'message': '密码至少需要6个字符'}
    
    users[username] = {
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'login_attempts': {'count': 0, 'last_attempt': None}
    }
    
    save_users(users)
    
    return {'success': True, 'message': '注册成功'}


def login_user(identifier, password):
    """
    @brief  用户登录
    @param  identifier: 用户名或邮箱
    @param  password: 密码
    @retval dict: 包含状态和消息的字典
    """
    users = load_users()
    username, user_data = find_user_by_username_or_email(users, identifier)
    
    if not user_data:
        return {'success': False, 'message': '用户名或密码错误'}
    
    lockout_status = check_login_attempts(users, username)
    if lockout_status['locked']:
        return {
            'success': False,
            'message': f"账户已锁定，请{lockout_status['remaining_time']}秒后重试",
            'locked': True,
            'remaining_time': lockout_status['remaining_time']
        }
    
    if not verify_password(password, user_data['password']):
        record_login_attempt(users, username, False)
        return {'success': False, 'message': '用户名或密码错误'}
    
    record_login_attempt(users, username, True)
    
    return {
        'success': True,
        'message': '登录成功',
        'username': username,
        'email': user_data['email']
    }


def create_reset_token(email):
    """
    @brief  创建密码重置令牌
    @param  email: 邮箱地址
    @retval dict: 包含状态和令牌的字典
    """
    users = load_users()
    
    for username, user_data in users.items():
        if user_data.get('email') == email:
            token = secrets.token_urlsafe(32)
            tokens = load_reset_tokens()
            
            tokens[token] = {
                'username': username,
                'email': email,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
            }
            
            save_reset_tokens(tokens)
            
            return {
                'success': True,
                'message': '重置密码链接已发送',
                'token': token
            }
    
    return {'success': False, 'message': '该邮箱未注册'}


def reset_password(token, new_password):
    """
    @brief  重置密码
    @param  token: 重置令牌
    @param  new_password: 新密码
    @retval dict: 包含状态和消息的字典
    """
    tokens = load_reset_tokens()
    
    if token not in tokens:
        return {'success': False, 'message': '无效的重置链接'}
    
    token_data = tokens[token]
    expires_at = datetime.fromisoformat(token_data['expires_at'])
    
    if datetime.now() > expires_at:
        del tokens[token]
        save_reset_tokens(tokens)
        return {'success': False, 'message': '重置链接已过期'}
    
    if len(new_password) < 6:
        return {'success': False, 'message': '密码至少需要6个字符'}
    
    users = load_users()
    username = token_data['username']
    
    users[username]['password'] = hash_password(new_password)
    users[username]['login_attempts'] = {'count': 0, 'last_attempt': None}
    save_users(users)
    
    del tokens[token]
    save_reset_tokens(tokens)
    
    return {'success': True, 'message': '密码重置成功'}
