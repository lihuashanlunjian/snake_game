"""
@file    validators.py
@brief   数据验证模块
@details 实现用户输入数据的验证逻辑，确保数据完整性和合法性
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserValidator:
    """
    @brief  用户数据验证器
    @details 验证用户名、邮箱、密码等数据的合法性
    """
    
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 50
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 128
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate_username(username):
        """
        @brief  验证用户名
        @param  username: 用户名
        @retval dict: 包含验证结果和错误信息的字典
        """
        if not username:
            return {'valid': False, 'message': '用户名不能为空'}
        
        if not isinstance(username, str):
            return {'valid': False, 'message': '用户名必须是字符串'}
        
        username = username.strip()
        
        if len(username) < UserValidator.USERNAME_MIN_LENGTH:
            return {'valid': False, 'message': f'用户名至少需要{UserValidator.USERNAME_MIN_LENGTH}个字符'}
        
        if len(username) > UserValidator.USERNAME_MAX_LENGTH:
            return {'valid': False, 'message': f'用户名不能超过{UserValidator.USERNAME_MAX_LENGTH}个字符'}
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return {'valid': False, 'message': '用户名只能包含字母、数字和下划线'}
        
        if username[0].isdigit():
            return {'valid': False, 'message': '用户名不能以数字开头'}
        
        logger.info(f"用户名验证通过: {username}")
        return {'valid': True, 'message': '用户名格式正确'}
    
    @staticmethod
    def validate_email(email):
        """
        @brief  验证邮箱地址
        @param  email: 邮箱地址
        @retval dict: 包含验证结果和错误信息的字典
        """
        if not email:
            return {'valid': False, 'message': '邮箱地址不能为空'}
        
        if not isinstance(email, str):
            return {'valid': False, 'message': '邮箱地址必须是字符串'}
        
        email = email.strip().lower()
        
        if not re.match(UserValidator.EMAIL_PATTERN, email):
            return {'valid': False, 'message': '邮箱地址格式不正确'}
        
        if len(email) > 120:
            return {'valid': False, 'message': '邮箱地址不能超过120个字符'}
        
        logger.info(f"邮箱验证通过: {email}")
        return {'valid': True, 'message': '邮箱格式正确'}
    
    @staticmethod
    def validate_password(password):
        """
        @brief  验证密码
        @param  password: 密码
        @retval dict: 包含验证结果和错误信息的字典
        """
        if not password:
            return {'valid': False, 'message': '密码不能为空'}
        
        if not isinstance(password, str):
            return {'valid': False, 'message': '密码必须是字符串'}
        
        if len(password) < UserValidator.PASSWORD_MIN_LENGTH:
            return {'valid': False, 'message': f'密码至少需要{UserValidator.PASSWORD_MIN_LENGTH}个字符'}
        
        if len(password) > UserValidator.PASSWORD_MAX_LENGTH:
            return {'valid': False, 'message': f'密码不能超过{UserValidator.PASSWORD_MAX_LENGTH}个字符'}
        
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_letter and has_digit):
            return {'valid': False, 'message': '密码必须包含字母和数字'}
        
        logger.info("密码验证通过")
        return {'valid': True, 'message': '密码格式正确'}
    
    @staticmethod
    def check_password_strength(password):
        """
        @brief  检查密码强度
        @param  password: 密码
        @retval dict: 包含强度等级和建议的字典
        """
        strength = 0
        suggestions = []
        
        if len(password) >= 8:
            strength += 1
        else:
            suggestions.append('建议密码长度至少8个字符')
        
        if len(password) >= 12:
            strength += 1
        
        if any(c.islower() for c in password):
            strength += 1
        else:
            suggestions.append('建议包含小写字母')
        
        if any(c.isupper() for c in password):
            strength += 1
        else:
            suggestions.append('建议包含大写字母')
        
        if any(c.isdigit() for c in password):
            strength += 1
        else:
            suggestions.append('建议包含数字')
        
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            strength += 1
        else:
            suggestions.append('建议包含特殊字符')
        
        if strength <= 2:
            level = '弱'
        elif strength <= 4:
            level = '中等'
        elif strength <= 5:
            level = '强'
        else:
            level = '非常强'
        
        return {
            'strength': strength,
            'level': level,
            'suggestions': suggestions
        }
    
    @staticmethod
    def validate_registration_data(username, email, password):
        """
        @brief  验证注册数据
        @param  username: 用户名
        @param  email: 邮箱地址
        @param  password: 密码
        @retval dict: 包含验证结果和错误信息的字典
        """
        username_result = UserValidator.validate_username(username)
        if not username_result['valid']:
            return username_result
        
        email_result = UserValidator.validate_email(email)
        if not email_result['valid']:
            return email_result
        
        password_result = UserValidator.validate_password(password)
        if not password_result['valid']:
            return password_result
        
        logger.info(f"注册数据验证通过: {username}, {email}")
        return {'valid': True, 'message': '注册数据验证通过'}
    
    @staticmethod
    def validate_login_data(identifier, password):
        """
        @brief  验证登录数据
        @param  identifier: 用户名或邮箱
        @param  password: 密码
        @retval dict: 包含验证结果和错误信息的字典
        """
        if not identifier:
            return {'valid': False, 'message': '用户名或邮箱不能为空'}
        
        if not password:
            return {'valid': False, 'message': '密码不能为空'}
        
        if not isinstance(identifier, str) or not isinstance(password, str):
            return {'valid': False, 'message': '输入数据格式不正确'}
        
        identifier = identifier.strip()
        
        if len(identifier) == 0:
            return {'valid': False, 'message': '用户名或邮箱不能为空'}
        
        if len(password) == 0:
            return {'valid': False, 'message': '密码不能为空'}
        
        logger.info(f"登录数据验证通过: {identifier}")
        return {'valid': True, 'message': '登录数据验证通过'}
    
    @staticmethod
    def sanitize_input(input_string):
        """
        @brief  清理输入数据
        @param  input_string: 输入字符串
        @retval str: 清理后的字符串
        """
        if not isinstance(input_string, str):
            return ''
        
        sanitized = input_string.strip()
        
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        
        return sanitized
