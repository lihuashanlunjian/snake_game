"""
@file    social_config.py
@brief   第三方登录配置模块
@details 微信开放平台和QQ互联平台的配置信息
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import os
from urllib.parse import quote


class WeChatConfig:
    """微信开放平台配置"""
    
    WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', '')
    WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', '')
    WECHAT_REDIRECT_URI = os.environ.get('WECHAT_REDIRECT_URI', 'http://localhost:5000/api/auth/wechat/callback')
    
    WECHAT_AUTH_URL = 'https://open.weixin.qq.com/connect/qrconnect'
    WECHAT_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    WECHAT_USERINFO_URL = 'https://api.weixin.qq.com/sns/userinfo'
    
    @classmethod
    def is_configured(cls):
        """检查微信配置是否完整"""
        return bool(cls.WECHAT_APP_ID and cls.WECHAT_APP_SECRET)
    
    @classmethod
    def get_authorization_url(cls, state='register'):
        """生成微信授权URL"""
        if not cls.is_configured():
            return None
        
        redirect_uri_encoded = quote(cls.WECHAT_REDIRECT_URI, safe='')
        
        params = {
            'appid': cls.WECHAT_APP_ID,
            'redirect_uri': redirect_uri_encoded,
            'response_type': 'code',
            'scope': 'snsapi_login',
            'state': state
        }
        
        param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{cls.WECHAT_AUTH_URL}?{param_str}#wechat_redirect"
    
    @classmethod
    def get_config_status(cls):
        """获取配置状态"""
        return {
            'app_id_configured': bool(cls.WECHAT_APP_ID),
            'app_secret_configured': bool(cls.WECHAT_APP_SECRET),
            'redirect_uri': cls.WECHAT_REDIRECT_URI,
            'is_ready': cls.is_configured()
        }


class QQConfig:
    """QQ互联平台配置"""
    
    QQ_APP_ID = os.environ.get('QQ_APP_ID', '')
    QQ_APP_KEY = os.environ.get('QQ_APP_KEY', '')
    QQ_REDIRECT_URI = os.environ.get('QQ_REDIRECT_URI', 'http://localhost:5000/api/auth/qq/callback')
    
    QQ_AUTH_URL = 'https://graph.qq.com/oauth2.0/authorize'
    QQ_ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
    QQ_OPENID_URL = 'https://graph.qq.com/oauth2.0/me'
    QQ_USERINFO_URL = 'https://graph.qq.com/user/get_user_info'
    
    @classmethod
    def is_configured(cls):
        """检查QQ配置是否完整"""
        return bool(cls.QQ_APP_ID and cls.QQ_APP_KEY)
    
    @classmethod
    def get_authorization_url(cls, state='register'):
        """生成QQ授权URL"""
        if not cls.is_configured():
            return None
        
        redirect_uri_encoded = quote(cls.QQ_REDIRECT_URI, safe='')
        
        params = {
            'response_type': 'code',
            'client_id': cls.QQ_APP_ID,
            'redirect_uri': redirect_uri_encoded,
            'scope': 'get_user_info',
            'state': state
        }
        
        param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{cls.QQ_AUTH_URL}?{param_str}"
    
    @classmethod
    def get_config_status(cls):
        """获取配置状态"""
        return {
            'app_id_configured': bool(cls.QQ_APP_ID),
            'app_key_configured': bool(cls.QQ_APP_KEY),
            'redirect_uri': cls.QQ_REDIRECT_URI,
            'is_ready': cls.is_configured()
        }


class SocialLoginService:
    """第三方登录服务"""
    
    @staticmethod
    def get_wechat_auth_response(action='register'):
        """获取微信授权响应"""
        if not WeChatConfig.is_configured():
            return {
                'success': False,
                'message': '微信登录未配置，请联系管理员配置AppID',
                'error_code': 'WECHAT_NOT_CONFIGURED',
                'config_guide': {
                    'step1': '访问微信开放平台 https://open.weixin.qq.com/',
                    'step2': '创建网站应用并获取AppID和AppSecret',
                    'step3': '设置环境变量 WECHAT_APP_ID 和 WECHAT_APP_SECRET',
                    'step4': '配置授权回调域名'
                }
            }
        
        auth_url = WeChatConfig.get_authorization_url(state=action)
        return {
            'success': True,
            'message': '微信授权已启动',
            'auth_url': auth_url,
            'expires_in': 300
        }
    
    @staticmethod
    def get_qq_auth_response(action='register'):
        """获取QQ授权响应"""
        if not QQConfig.is_configured():
            return {
                'success': False,
                'message': 'QQ登录未配置，请联系管理员配置AppID',
                'error_code': 'QQ_NOT_CONFIGURED',
                'config_guide': {
                    'step1': '访问QQ互联平台 https://connect.qq.com/',
                    'step2': '创建网站应用并获取AppID和AppKey',
                    'step3': '设置环境变量 QQ_APP_ID 和 QQ_APP_KEY',
                    'step4': '配置授权回调地址'
                }
            }
        
        auth_url = QQConfig.get_authorization_url(state=action)
        return {
            'success': True,
            'message': 'QQ授权已启动',
            'auth_url': auth_url,
            'expires_in': 300
        }
    
    @staticmethod
    def get_config_status():
        """获取所有第三方登录配置状态"""
        return {
            'wechat': WeChatConfig.get_config_status(),
            'qq': QQConfig.get_config_status()
        }
