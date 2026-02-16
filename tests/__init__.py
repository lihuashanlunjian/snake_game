"""
@file    __init__.py
@brief   测试模块初始化
@details 导出测试类
@author  AI Assistant
@date    2026-02-16
@version V1.0.0
"""

from .test_snake_game import *

__all__ = [
    'TestSnakeGameInit',
    'TestSnakeGamePause',
    'TestSnakeGameStart',
    'TestSnakeGameReset',
    'TestSnakeGameDirection',
    'TestSnakeGameCollision',
    'TestSnakeGameScore',
    'TestSnakeGameGetState'
]
