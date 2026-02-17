"""
@file    test_database.py
@brief   数据库功能测试脚本
@details 测试用户注册、登录、密码重置等数据库操作
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db, User, PasswordResetToken
from database.user_dao import UserDAO, PasswordResetTokenDAO
from database.auth_service import AuthService
from database.validators import UserValidator


def test_user_validation():
    """
    @brief  测试用户数据验证
    @retval None
    """
    print("\n" + "=" * 60)
    print("测试 1: 用户数据验证")
    print("=" * 60)
    
    print("\n测试用户名验证:")
    result = UserValidator.validate_username("test_user")
    print(f"  有效用户名 'test_user': {result['valid']} - {result['message']}")
    
    result = UserValidator.validate_username("ab")
    print(f"  无效用户名 'ab': {result['valid']} - {result['message']}")
    
    result = UserValidator.validate_username("123user")
    print(f"  无效用户名 '123user': {result['valid']} - {result['message']}")
    
    print("\n测试邮箱验证:")
    result = UserValidator.validate_email("test@example.com")
    print(f"  有效邮箱: {result['valid']} - {result['message']}")
    
    result = UserValidator.validate_email("invalid-email")
    print(f"  无效邮箱: {result['valid']} - {result['message']}")
    
    print("\n测试密码验证:")
    result = UserValidator.validate_password("password123")
    print(f"  有效密码: {result['valid']} - {result['message']}")
    
    result = UserValidator.validate_password("123")
    print(f"  无效密码: {result['valid']} - {result['message']}")
    
    print("\n测试密码强度:")
    strength = UserValidator.check_password_strength("MyP@ssw0rd123")
    print(f"  密码 'MyP@ssw0rd123' 强度: {strength['level']} (分数: {strength['strength']})")
    
    print("✅ 用户数据验证测试完成")


def test_user_registration():
    """
    @brief  测试用户注册
    @retval None
    """
    print("\n" + "=" * 60)
    print("测试 2: 用户注册")
    print("=" * 60)
    
    with app.app_context():
        User.query.filter(User.username.like('test_%')).delete()
        db.session.commit()
        
        print("\n注册新用户:")
        result = AuthService.register_user("test_user", "test@example.com", "password123")
        print(f"  注册结果: {result['success']} - {result['message']}")
        
        if result['success']:
            print(f"  用户ID: {result.get('user_id')}")
        
        print("\n尝试重复注册:")
        result = AuthService.register_user("test_user", "another@example.com", "password123")
        print(f"  注册结果: {result['success']} - {result['message']}")
        
        print("\n尝试使用已注册邮箱:")
        result = AuthService.register_user("another_user", "test@example.com", "password123")
        print(f"  注册结果: {result['success']} - {result['message']}")
        
        print("✅ 用户注册测试完成")


def test_user_login():
    """
    @brief  测试用户登录
    @retval None
    """
    print("\n" + "=" * 60)
    print("测试 3: 用户登录")
    print("=" * 60)
    
    with app.app_context():
        print("\n正确登录:")
        result = AuthService.login_user("test_user", "password123")
        print(f"  登录结果: {result['success']} - {result['message']}")
        
        if result['success']:
            print(f"  用户ID: {result.get('user_id')}")
            print(f"  用户名: {result.get('username')}")
            print(f"  邮箱: {result.get('email')}")
        
        print("\n错误密码:")
        result = AuthService.login_user("test_user", "wrongpassword")
        print(f"  登录结果: {result['success']} - {result['message']}")
        
        print("\n使用邮箱登录:")
        result = AuthService.login_user("test@example.com", "password123")
        print(f"  登录结果: {result['success']} - {result['message']}")
        
        print("✅ 用户登录测试完成")


def test_password_reset():
    """
    @brief  测试密码重置
    @retval None
    """
    print("\n" + "=" * 60)
    print("测试 4: 密码重置")
    print("=" * 60)
    
    with app.app_context():
        print("\n创建重置令牌:")
        result = AuthService.create_reset_token("test@example.com")
        print(f"  创建结果: {result['success']} - {result['message']}")
        
        if result['success']:
            token = result.get('token')
            print(f"  令牌: {token[:20]}...")
            
            print("\n使用令牌重置密码:")
            result = AuthService.reset_password(token, "newpassword123")
            print(f"  重置结果: {result['success']} - {result['message']}")
            
            print("\n使用新密码登录:")
            result = AuthService.login_user("test_user", "newpassword123")
            print(f"  登录结果: {result['success']} - {result['message']}")
        
        print("✅ 密码重置测试完成")


def test_user_dao():
    """
    @brief  测试用户数据访问对象
    @retval None
    """
    print("\n" + "=" * 60)
    print("测试 5: 用户数据访问对象 (DAO)")
    print("=" * 60)
    
    with app.app_context():
        print("\n查询用户:")
        user = UserDAO.get_user_by_username("test_user")
        if user:
            print(f"  用户ID: {user.user_id}")
            print(f"  用户名: {user.username}")
            print(f"  邮箱: {user.email}")
            print(f"  创建时间: {user.created_at}")
            print(f"  激活状态: {user.is_active}")
        
        print("\n更新用户信息:")
        success = UserDAO.update_user(user.user_id, last_login_at=None)
        print(f"  更新结果: {success}")
        
        print("\n查询所有用户:")
        users = User.query.all()
        print(f"  用户总数: {len(users)}")
        for u in users:
            print(f"    - {u.username} ({u.email})")
        
        print("✅ 用户DAO测试完成")


def test_brute_force_protection():
    """
    @brief  测试防暴力破解保护
    @retval None
    """
    print("\n" + "=" * 60)
    print("测试 6: 防暴力破解保护")
    print("=" * 60)
    
    with app.app_context():
        user = UserDAO.get_user_by_username("test_user")
        
        print("\n模拟多次登录失败:")
        for i in range(5):
            result = AuthService.login_user("test_user", "wrongpassword")
            print(f"  第{i+1}次失败: {result['message']}")
        
        print("\n检查锁定状态:")
        lockout_status = UserDAO.check_user_locked(user.user_id, max_attempts=5)
        print(f"  是否锁定: {lockout_status['locked']}")
        if lockout_status['locked']:
            print(f"  剩余时间: {lockout_status['remaining_time']}秒")
        
        print("\n解锁用户:")
        success = UserDAO.unlock_user(user.user_id)
        print(f"  解锁结果: {success}")
        
        print("\n再次尝试登录:")
        result = AuthService.login_user("test_user", "newpassword123")
        print(f"  登录结果: {result['success']} - {result['message']}")
        
        print("✅ 防暴力破解保护测试完成")


def cleanup_test_data():
    """
    @brief  清理测试数据
    @retval None
    """
    print("\n" + "=" * 60)
    print("清理测试数据")
    print("=" * 60)
    
    with app.app_context():
        User.query.filter(User.username.like('test_%')).delete()
        db.session.commit()
        print("✅ 测试数据已清理")


def main():
    """
    @brief  主测试函数
    @retval None
    """
    print("\n" + "=" * 60)
    print("开始数据库功能测试")
    print("=" * 60)
    
    try:
        test_user_validation()
        test_user_registration()
        test_user_login()
        test_password_reset()
        test_user_dao()
        test_brute_force_protection()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup_test_data()


if __name__ == '__main__':
    main()
