"""
@file    __init__.py
@brief   游戏模块初始化
@details 导出游戏核心类
@author  AI Assistant
@date    2026-02-16
@version V1.0.0
"""

# 从当前包中导入贪吃蛇游戏核心类
from .snake_game import SnakeGame

# 定义模块的公开接口，限制外部使用from module import *时导入的内容
__all__ = ['SnakeGame']
