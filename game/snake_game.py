"""
@file    snake_game.py
@brief   贪吃蛇游戏核心逻辑
@details 实现蛇的移动、食物生成、碰撞检测、得分计算等核心功能
@author  AI Assistant
@date    2026-02-16
@version V1.0.0
"""

# 导入随机数模块，用于随机生成食物位置
import random

# 导入JSON模块，用于保存和加载最高分
import json

# 导入操作系统模块，用于文件操作
import os

# 导入枚举类，用于定义方向和游戏状态
from enum import Enum

# 导入类型提示模块，用于代码可读性和类型检查
from typing import List, Tuple, Optional


# 定义蛇的移动方向枚举类
class Direction_e(Enum):
    # 向上移动
    UP = 'up'
    # 向下移动
    DOWN = 'down'
    # 向左移动
    LEFT = 'left'
    # 向右移动
    RIGHT = 'right'


# 定义游戏状态枚举类
class GameState_e(Enum):
    # 空闲状态，游戏未开始
    IDLE = 'idle'
    # 游戏进行中
    PLAYING = 'playing'
    # 游戏暂停
    PAUSED = 'paused'
    # 游戏结束
    GAME_OVER = 'game_over'


# 定义游戏网格宽度（格子数）
GRID_WIDTH = 20

# 定义游戏网格高度（格子数）
GRID_HEIGHT = 20

# 定义每个格子的像素大小
CELL_SIZE = 20

# 定义蛇的初始长度
INITIAL_SNAKE_LENGTH = 3

# 定义游戏更新速度（毫秒）
GAME_SPEED = 150


class SnakeGame:
    """
    @brief  贪吃蛇游戏类
    @details 包含游戏所有核心逻辑
    """
    
    def __init__(self):
        """@brief  初始化游戏实例"""
        # 蛇身体坐标列表，每个元素是一个(x, y)元组
        self.snake_body: List[Tuple[int, int]] = []
        # 食物位置坐标
        self.food_position: Tuple[int, int] = (0, 0)
        # 当前移动方向，默认向右
        self.current_direction: Direction_e = Direction_e.RIGHT
        # 下一步移动方向，用于防止快速按键导致反向移动
        self.next_direction: Direction_e = Direction_e.RIGHT
        # 当前得分
        self.score: int = 0
        # 历史最高分
        self.highscore: int = 0
        # 当前游戏状态
        self.game_state: GameState_e = GameState_e.IDLE
        # 网格宽度
        self.grid_width: int = GRID_WIDTH
        # 网格高度
        self.grid_height: int = GRID_HEIGHT
        # 加载历史最高分
        self._load_highscore()
    
    def _load_highscore(self) -> None:
        """
        @brief  从文件加载历史最高分
        @retval None
        """
        try:
            # 检查最高分文件是否存在
            if os.path.exists('highscore.json'):
                # 打开文件并读取JSON数据
                with open('highscore.json', 'r') as f:
                    # 解析JSON数据
                    data = json.load(f)
                    # 获取最高分，如果不存在则默认为0
                    self.highscore = data.get('highscore', 0)
        # 捕获IO错误和JSON解析错误
        except (IOError, json.JSONDecodeError):
            # 发生错误时，最高分重置为0
            self.highscore = 0
    
    def _save_highscore(self) -> None:
        """
        @brief  保存最高分到文件
        @retval None
        """
        try:
            # 打开文件并写入JSON数据
            with open('highscore.json', 'w') as f:
                # 将最高分以JSON格式写入文件
                json.dump({'highscore': self.highscore}, f)
        # 捕获IO错误，忽略保存失败
        except IOError:
            pass
    
    def reset(self) -> None:
        """
        @brief  重置游戏状态到初始状态
        @retval None
        """
        # 计算网格中心X坐标
        center_x = self.grid_width // 2
        # 计算网格中心Y坐标
        center_y = self.grid_height // 2
        # 初始化蛇身体，从中心位置开始，向左延伸
        self.snake_body = [
            (center_x - i, center_y) 
            for i in range(INITIAL_SNAKE_LENGTH)
        ]
        # 重置当前方向为向右
        self.current_direction = Direction_e.RIGHT
        # 重置下一步方向为向右
        self.next_direction = Direction_e.RIGHT
        # 重置得分为0
        self.score = 0
        # 设置游戏状态为空闲
        self.game_state = GameState_e.IDLE
        # 生成新的食物
        self._spawn_food()
    
    def start(self) -> None:
        """
        @brief  开始游戏
        @retval None
        """
        # 只有在空闲或游戏结束状态才能开始
        if self.game_state == GameState_e.IDLE or self.game_state == GameState_e.GAME_OVER:
            # 设置游戏状态为进行中
            self.game_state = GameState_e.PLAYING
    
    def toggle_pause(self) -> None:
        """
        @brief  切换游戏暂停状态
        @retval None
        """
        # 如果正在游戏中，则暂停
        if self.game_state == GameState_e.PLAYING:
            self.game_state = GameState_e.PAUSED
        # 如果已暂停，则继续游戏
        elif self.game_state == GameState_e.PAUSED:
            self.game_state = GameState_e.PLAYING
    
    def set_direction(self, direction: str) -> None:
        """
        @brief  设置蛇的移动方向
        @param  direction: 方向字符串 ('up', 'down', 'left', 'right')
        @retval None
        """
        # 方向字符串到枚举值的映射
        direction_map = {
            'up': Direction_e.UP,
            'down': Direction_e.DOWN,
            'left': Direction_e.LEFT,
            'right': Direction_e.RIGHT
        }
        
        # 如果传入的方向无效，直接返回
        if direction not in direction_map:
            return
        
        # 获取对应的方向枚举值
        new_direction = direction_map[direction]
        
        # 定义相反方向映射，防止蛇反向移动
        opposite_directions = {
            Direction_e.UP: Direction_e.DOWN,
            Direction_e.DOWN: Direction_e.UP,
            Direction_e.LEFT: Direction_e.RIGHT,
            Direction_e.RIGHT: Direction_e.LEFT
        }
        
        # 只有新方向不是当前方向的相反方向时才更新
        if opposite_directions.get(new_direction) != self.current_direction:
            self.next_direction = new_direction
    
    def _spawn_food(self) -> None:
        """
        @brief  在随机位置生成食物
        @retval None
        """
        # 获取所有可用的位置（不在蛇身上的位置）
        available_positions = [
            (x, y) 
            for x in range(self.grid_width) 
            for y in range(self.grid_height) 
            if (x, y) not in self.snake_body
        ]
        
        # 如果有可用位置，随机选择一个
        if available_positions:
            self.food_position = random.choice(available_positions)
    
    def _check_collision(self, position: Tuple[int, int]) -> bool:
        """
        @brief  检查指定位置是否发生碰撞
        @param  position: 要检查的位置坐标
        @retval true: 发生碰撞, false: 无碰撞
        """
        # 解构位置坐标
        x, y = position
        
        # 检查是否撞到左边界或右边界
        if x < 0 or x >= self.grid_width:
            return True
        # 检查是否撞到上边界或下边界
        if y < 0 or y >= self.grid_height:
            return True
        # 检查是否撞到蛇身体（排除蛇头）
        if position in self.snake_body[:-1]:
            return True
        
        # 无碰撞
        return False
    
    def update(self) -> None:
        """
        @brief  更新游戏状态，每帧调用一次
        @retval None
        """
        # 如果游戏不在进行中，不执行更新
        if self.game_state != GameState_e.PLAYING:
            return
        
        # 更新当前方向为下一步方向
        self.current_direction = self.next_direction
        
        # 获取蛇头当前坐标
        head_x, head_y = self.snake_body[0]
        
        # 定义各方向对应的坐标偏移量
        direction_offsets = {
            Direction_e.UP: (0, -1),
            Direction_e.DOWN: (0, 1),
            Direction_e.LEFT: (-1, 0),
            Direction_e.RIGHT: (1, 0)
        }
        
        # 获取当前方向的偏移量
        dx, dy = direction_offsets[self.current_direction]
        # 计算新的蛇头位置
        new_head = (head_x + dx, head_y + dy)
        
        # 检查新位置是否发生碰撞
        if self._check_collision(new_head):
            # 设置游戏状态为结束
            self.game_state = GameState_e.GAME_OVER
            # 如果当前得分超过最高分，更新并保存
            if self.score > self.highscore:
                self.highscore = self.score
                self._save_highscore()
            return
        
        # 将新头部位置插入到蛇身体列表开头
        self.snake_body.insert(0, new_head)
        
        # 检查是否吃到食物
        if new_head == self.food_position:
            # 增加得分
            self.score += 10
            # 生成新的食物
            self._spawn_food()
        else:
            # 没吃到食物，移除尾部（保持长度不变）
            self.snake_body.pop()
    
    def get_state(self) -> dict:
        """
        @brief  获取当前游戏状态的完整信息
        @retval 包含游戏状态的字典
        """
        return {
            # 蛇身体坐标列表
            'snake_body': self.snake_body,
            # 食物位置
            'food_position': self.food_position,
            # 当前移动方向
            'direction': self.current_direction.value,
            # 当前得分
            'score': self.score,
            # 历史最高分
            'highscore': self.highscore,
            # 游戏状态
            'game_state': self.game_state.value,
            # 网格宽度
            'grid_width': self.grid_width,
            # 网格高度
            'grid_height': self.grid_height,
            # 格子大小
            'cell_size': CELL_SIZE
        }
    
    def get_highscore(self) -> int:
        """
        @brief  获取历史最高分
        @retval 最高分数值
        """
        return self.highscore
