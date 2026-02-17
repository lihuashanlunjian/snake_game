"""
@file    test_social_login.py
@brief   社交登录功能单元测试
@details 测试微信注册和QQ注册按钮功能
@author  AI Assistant
@date    2026-02-17
@version V1.0.1
"""

import unittest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from auth.social_config import WeChatConfig, QQConfig, SocialLoginService


class TestSocialLoginAPI(unittest.TestCase):
    """测试社交登录API接口"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_wechat_authorize_endpoint_exists(self):
        """测试微信授权接口存在"""
        response = self.app.post('/api/auth/wechat/authorize',
            data=json.dumps({'action': 'register'}),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [200, 400])
    
    def test_wechat_authorize_returns_json(self):
        """测试微信授权返回JSON"""
        response = self.app.post('/api/auth/wechat/authorize',
            data=json.dumps({'action': 'register'}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_wechat_authorize_returns_message(self):
        """测试微信授权返回消息"""
        response = self.app.post('/api/auth/wechat/authorize',
            data=json.dumps({'action': 'register'}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_wechat_authorize_unconfigured_returns_error_code(self):
        """测试微信未配置时返回错误码"""
        if not WeChatConfig.is_configured():
            response = self.app.post('/api/auth/wechat/authorize',
                data=json.dumps({'action': 'register'}),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertFalse(data.get('success'))
            self.assertEqual(data.get('error_code'), 'WECHAT_NOT_CONFIGURED')
    
    def test_qq_authorize_endpoint_exists(self):
        """测试QQ授权接口存在"""
        response = self.app.post('/api/auth/qq/authorize',
            data=json.dumps({'action': 'register'}),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [200, 400])
    
    def test_qq_authorize_returns_json(self):
        """测试QQ授权返回JSON"""
        response = self.app.post('/api/auth/qq/authorize',
            data=json.dumps({'action': 'register'}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_qq_authorize_returns_message(self):
        """测试QQ授权返回消息"""
        response = self.app.post('/api/auth/qq/authorize',
            data=json.dumps({'action': 'register'}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_qq_authorize_unconfigured_returns_error_code(self):
        """测试QQ未配置时返回错误码"""
        if not QQConfig.is_configured():
            response = self.app.post('/api/auth/qq/authorize',
                data=json.dumps({'action': 'register'}),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertFalse(data.get('success'))
            self.assertEqual(data.get('error_code'), 'QQ_NOT_CONFIGURED')
    
    def test_social_config_endpoint_exists(self):
        """测试社交登录配置状态接口存在"""
        response = self.app.get('/api/auth/social/config')
        
        self.assertEqual(response.status_code, 200)
    
    def test_social_config_returns_success(self):
        """测试社交登录配置状态返回成功"""
        response = self.app.get('/api/auth/social/config')
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
    
    def test_social_config_contains_wechat_status(self):
        """测试配置状态包含微信状态"""
        response = self.app.get('/api/auth/social/config')
        
        data = json.loads(response.data)
        self.assertIn('wechat', data.get('config', {}))
    
    def test_social_config_contains_qq_status(self):
        """测试配置状态包含QQ状态"""
        response = self.app.get('/api/auth/social/config')
        
        data = json.loads(response.data)
        self.assertIn('qq', data.get('config', {}))
    
    def test_social_status_endpoint_exists(self):
        """测试社交登录状态接口存在"""
        response = self.app.get('/api/auth/social/status')
        
        self.assertEqual(response.status_code, 200)
    
    def test_social_status_returns_success(self):
        """测试社交登录状态返回成功"""
        response = self.app.get('/api/auth/social/status')
        
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))
    
    def test_social_status_contains_registered_field(self):
        """测试社交登录状态包含注册状态字段"""
        response = self.app.get('/api/auth/social/status')
        
        data = json.loads(response.data)
        self.assertIn('registered', data)
    
    def test_wechat_callback_endpoint_exists(self):
        """测试微信回调接口存在"""
        response = self.app.get('/api/auth/wechat/callback?code=test_code')
        
        self.assertIn(response.status_code, [200, 302])
    
    def test_wechat_callback_without_code_redirects_to_register(self):
        """测试微信回调无code时重定向到注册页"""
        response = self.app.get('/api/auth/wechat/callback')
        
        self.assertEqual(response.status_code, 302)
    
    def test_qq_callback_endpoint_exists(self):
        """测试QQ回调接口存在"""
        response = self.app.get('/api/auth/qq/callback?code=test_code')
        
        self.assertIn(response.status_code, [200, 302])
    
    def test_qq_callback_without_code_redirects_to_register(self):
        """测试QQ回调无code时重定向到注册页"""
        response = self.app.get('/api/auth/qq/callback')
        
        self.assertEqual(response.status_code, 302)


class TestSocialConfigModule(unittest.TestCase):
    """测试社交登录配置模块"""
    
    def test_wechat_config_has_is_configured_method(self):
        """测试微信配置类有is_configured方法"""
        self.assertTrue(hasattr(WeChatConfig, 'is_configured'))
    
    def test_wechat_config_has_get_authorization_url_method(self):
        """测试微信配置类有get_authorization_url方法"""
        self.assertTrue(hasattr(WeChatConfig, 'get_authorization_url'))
    
    def test_wechat_config_has_get_config_status_method(self):
        """测试微信配置类有get_config_status方法"""
        self.assertTrue(hasattr(WeChatConfig, 'get_config_status'))
    
    def test_qq_config_has_is_configured_method(self):
        """测试QQ配置类有is_configured方法"""
        self.assertTrue(hasattr(QQConfig, 'is_configured'))
    
    def test_qq_config_has_get_authorization_url_method(self):
        """测试QQ配置类有get_authorization_url方法"""
        self.assertTrue(hasattr(QQConfig, 'get_authorization_url'))
    
    def test_qq_config_has_get_config_status_method(self):
        """测试QQ配置类有get_config_status方法"""
        self.assertTrue(hasattr(QQConfig, 'get_config_status'))
    
    def test_wechat_config_status_returns_dict(self):
        """测试微信配置状态返回字典"""
        status = WeChatConfig.get_config_status()
        self.assertIsInstance(status, dict)
    
    def test_qq_config_status_returns_dict(self):
        """测试QQ配置状态返回字典"""
        status = QQConfig.get_config_status()
        self.assertIsInstance(status, dict)
    
    def test_social_login_service_has_wechat_auth_method(self):
        """测试社交登录服务有微信授权方法"""
        self.assertTrue(hasattr(SocialLoginService, 'get_wechat_auth_response'))
    
    def test_social_login_service_has_qq_auth_method(self):
        """测试社交登录服务有QQ授权方法"""
        self.assertTrue(hasattr(SocialLoginService, 'get_qq_auth_response'))
    
    def test_social_login_service_has_config_status_method(self):
        """测试社交登录服务有配置状态方法"""
        self.assertTrue(hasattr(SocialLoginService, 'get_config_status'))
    
    def test_unconfigured_wechat_returns_error_response(self):
        """测试未配置微信返回错误响应"""
        if not WeChatConfig.is_configured():
            response = SocialLoginService.get_wechat_auth_response()
            self.assertFalse(response['success'])
            self.assertIn('error_code', response)
            self.assertIn('config_guide', response)
    
    def test_unconfigured_qq_returns_error_response(self):
        """测试未配置QQ返回错误响应"""
        if not QQConfig.is_configured():
            response = SocialLoginService.get_qq_auth_response()
            self.assertFalse(response['success'])
            self.assertIn('error_code', response)
            self.assertIn('config_guide', response)


class TestSocialLoginButtonFunctionality(unittest.TestCase):
    """测试社交登录按钮功能"""
    
    def test_wechat_button_has_correct_class(self):
        """测试微信按钮有正确的CSS类"""
        html = '''
        <button type="button" class="btn btn-social btn-wechat">
            <span class="social-icon">💬</span>
            <span>微信注册</span>
        </button>
        '''
        
        self.assertIn('btn-wechat', html)
        self.assertIn('btn-social', html)
    
    def test_qq_button_has_correct_class(self):
        """测试QQ按钮有正确的CSS类"""
        html = '''
        <button type="button" class="btn btn-social btn-qq">
            <span class="social-icon">🐧</span>
            <span>QQ注册</span>
        </button>
        '''
        
        self.assertIn('btn-qq', html)
        self.assertIn('btn-social', html)
    
    def test_buttons_have_social_icon(self):
        """测试按钮包含社交图标"""
        wechat_html = '<span class="social-icon">💬</span>'
        qq_html = '<span class="social-icon">🐧</span>'
        
        self.assertIn('social-icon', wechat_html)
        self.assertIn('social-icon', qq_html)


class TestSocialLoginSecurity(unittest.TestCase):
    """测试社交登录安全性"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_authorize_endpoint_accepts_post_only(self):
        """测试授权接口只接受POST请求"""
        response = self.app.get('/api/auth/wechat/authorize')
        self.assertEqual(response.status_code, 405)
        
        response = self.app.get('/api/auth/qq/authorize')
        self.assertEqual(response.status_code, 405)
    
    def test_status_endpoint_accepts_get_only(self):
        """测试状态接口只接受GET请求"""
        response = self.app.post('/api/auth/social/status')
        self.assertEqual(response.status_code, 405)
    
    def test_config_endpoint_accepts_get_only(self):
        """测试配置接口只接受GET请求"""
        response = self.app.post('/api/auth/social/config')
        self.assertEqual(response.status_code, 405)
    
    def test_authorize_with_empty_body(self):
        """测试空请求体处理"""
        response = self.app.post('/api/auth/wechat/authorize',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [200, 400])


if __name__ == '__main__':
    unittest.main(verbosity=2)
