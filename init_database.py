"""
@file    init_database.py
@brief   数据库初始化脚本
@details 初始化数据库表结构，迁移现有JSON用户数据到数据库
@author  AI Assistant
@date    2026-02-17
@version V1.0.0
"""

import os
import sys
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db, User, PasswordResetToken
from database.auth_service import AuthService

USERS_FILE = 'users.json'
RESET_TOKENS_FILE = 'reset_tokens.json'


def init_database():
    """
    @brief  初始化数据库表结构
    @retval None
    """
    with app.app_context():
        try:
            db.create_all()
            logger.info("✅ 数据库表创建成功")
        except Exception as e:
            logger.error(f"❌ 数据库表创建失败: {str(e)}")
            raise


def migrate_users_from_json():
    """
    @brief  从JSON文件迁移用户数据到数据库
    @retval int: 迁移的用户数量
    """
    if not os.path.exists(USERS_FILE):
        logger.info("⚠️  未找到用户JSON文件，跳过迁移")
        return 0
    
    with app.app_context():
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            migrated_count = 0
            
            for username, user_data in users_data.items():
                existing_user = User.query.filter_by(username=username).first()
                
                if existing_user:
                    logger.info(f"⚠️  用户 {username} 已存在，跳过")
                    continue
                
                created_at = None
                if user_data.get('created_at'):
                    try:
                        created_at = datetime.fromisoformat(user_data['created_at'])
                    except:
                        created_at = datetime.utcnow()
                
                last_login_at = None
                login_attempt_count = 0
                last_login_attempt_at = None
                
                if user_data.get('login_attempts'):
                    login_attempt_count = user_data['login_attempts'].get('count', 0)
                    if user_data['login_attempts'].get('last_attempt'):
                        try:
                            last_login_attempt_at = datetime.fromisoformat(
                                user_data['login_attempts']['last_attempt']
                            )
                        except:
                            pass
                
                user = User(
                    username=username,
                    email=user_data.get('email', ''),
                    password_hash=user_data.get('password', ''),
                    created_at=created_at,
                    last_login_at=last_login_at,
                    login_attempt_count=login_attempt_count,
                    last_login_attempt_at=last_login_attempt_at,
                    is_active=True,
                    is_locked=False
                )
                
                db.session.add(user)
                migrated_count += 1
                logger.info(f"✅ 迁移用户: {username}")
            
            db.session.commit()
            logger.info(f"✅ 成功迁移 {migrated_count} 个用户")
            return migrated_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ 用户迁移失败: {str(e)}")
            return 0


def migrate_reset_tokens_from_json():
    """
    @brief  从JSON文件迁移密码重置令牌到数据库
    @retval int: 迁移的令牌数量
    """
    if not os.path.exists(RESET_TOKENS_FILE):
        logger.info("⚠️  未找到重置令牌JSON文件，跳过迁移")
        return 0
    
    with app.app_context():
        try:
            with open(RESET_TOKENS_FILE, 'r', encoding='utf-8') as f:
                tokens_data = json.load(f)
            
            migrated_count = 0
            
            for token, token_data in tokens_data.items():
                user = User.query.filter_by(username=token_data.get('username')).first()
                
                if not user:
                    logger.warning(f"⚠️  令牌对应的用户不存在: {token_data.get('username')}")
                    continue
                
                created_at = None
                expires_at = None
                
                if token_data.get('created_at'):
                    try:
                        created_at = datetime.fromisoformat(token_data['created_at'])
                    except:
                        created_at = datetime.utcnow()
                
                if token_data.get('expires_at'):
                    try:
                        expires_at = datetime.fromisoformat(token_data['expires_at'])
                    except:
                        expires_at = datetime.utcnow()
                
                reset_token = PasswordResetToken(
                    token=token,
                    user_id=user.user_id,
                    created_at=created_at,
                    expires_at=expires_at,
                    is_used=False
                )
                
                db.session.add(reset_token)
                migrated_count += 1
                logger.info(f"✅ 迁移令牌: {token[:10]}...")
            
            db.session.commit()
            logger.info(f"✅ 成功迁移 {migrated_count} 个令牌")
            return migrated_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ 令牌迁移失败: {str(e)}")
            return 0


def backup_json_files():
    """
    @brief  备份JSON文件
    @retval None
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if os.path.exists(USERS_FILE):
        backup_name = f"{USERS_FILE}.backup_{timestamp}"
        os.rename(USERS_FILE, backup_name)
        logger.info(f"✅ 已备份用户文件: {backup_name}")
    
    if os.path.exists(RESET_TOKENS_FILE):
        backup_name = f"{RESET_TOKENS_FILE}.backup_{timestamp}"
        os.rename(RESET_TOKENS_FILE, backup_name)
        logger.info(f"✅ 已备份令牌文件: {backup_name}")


def main():
    """
    @brief  主函数
    @retval None
    """
    logger.info("=" * 60)
    logger.info("开始数据库初始化和迁移")
    logger.info("=" * 60)
    
    logger.info("\n步骤 1: 初始化数据库表结构")
    init_database()
    
    logger.info("\n步骤 2: 迁移用户数据")
    user_count = migrate_users_from_json()
    
    logger.info("\n步骤 3: 迁移密码重置令牌")
    token_count = migrate_reset_tokens_from_json()
    
    if user_count > 0 or token_count > 0:
        logger.info("\n步骤 4: 备份JSON文件")
        backup_json_files()
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 数据库初始化和迁移完成")
    logger.info(f"   - 迁移用户数: {user_count}")
    logger.info(f"   - 迁移令牌数: {token_count}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
