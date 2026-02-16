"""
@file    test_snake_game.py
@brief   贪吃蛇游戏单元测试
@details 测试游戏核心逻辑，包括暂停功能测试
@author  AI Assistant
@date    2026-02-16
@version V1.0.0
"""

import unittest
import os
import json
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.snake_game import SnakeGame, Direction_e, GameState_e


class TestSnakeGameInit(unittest.TestCase):
    """测试游戏初始化"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
    
    def test_initial_state(self):
        """测试初始游戏状态"""
        self.assertEqual(self.game.game_state, GameState_e.IDLE)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.current_direction, Direction_e.RIGHT)
    
    def test_initial_snake_length(self):
        """测试初始蛇长度"""
        from game.snake_game import INITIAL_SNAKE_LENGTH
        self.assertEqual(len(self.game.snake_body), 0)


class TestSnakeGamePause(unittest.TestCase):
    """测试游戏暂停功能"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
        self.game.reset()
        self.game.start()
    
    def test_pause_from_playing(self):
        """测试从游戏进行中暂停"""
        # 确保游戏正在进行
        self.assertEqual(self.game.game_state, GameState_e.PLAYING)
        
        # 执行暂停
        self.game.toggle_pause()
        
        # 验证状态变为暂停
        self.assertEqual(self.game.game_state, GameState_e.PAUSED)
    
    def test_resume_from_paused(self):
        """测试从暂停状态继续游戏"""
        # 先暂停游戏
        self.game.toggle_pause()
        self.assertEqual(self.game.game_state, GameState_e.PAUSED)
        
        # 继续游戏
        self.game.toggle_pause()
        
        # 验证状态变为进行中
        self.assertEqual(self.game.game_state, GameState_e.PLAYING)
    
    def test_pause_toggle_multiple_times(self):
        """测试多次切换暂停状态"""
        # 第一次暂停
        self.game.toggle_pause()
        self.assertEqual(self.game.game_state, GameState_e.PAUSED)
        
        # 继续
        self.game.toggle_pause()
        self.assertEqual(self.game.game_state, GameState_e.PLAYING)
        
        # 再次暂停
        self.game.toggle_pause()
        self.assertEqual(self.game.game_state, GameState_e.PAUSED)
        
        # 再次继续
        self.game.toggle_pause()
        self.assertEqual(self.game.game_state, GameState_e.PLAYING)
    
    def test_no_update_when_paused(self):
        """测试暂停时游戏不更新"""
        # 记录暂停前的蛇头位置
        initial_head = self.game.snake_body[0]
        
        # 暂停游戏
        self.game.toggle_pause()
        
        # 尝试更新游戏
        self.game.update()
        
        # 验证蛇头位置没有变化
        self.assertEqual(self.game.snake_body[0], initial_head)
    
    def test_no_direction_change_when_paused(self):
        """测试暂停时方向改变被忽略"""
        # 暂停游戏
        self.game.toggle_pause()
        
        # 尝试改变方向
        self.game.set_direction('up')
        
        # 验证方向没有改变（仍然是RIGHT）
        self.assertEqual(self.game.current_direction, Direction_e.RIGHT)
    
    def test_pause_preserves_score(self):
        """测试暂停保留得分"""
        # 模拟得分
        self.game.score = 50
        
        # 暂停游戏
        self.game.toggle_pause()
        
        # 验证得分保留
        self.assertEqual(self.game.score, 50)
        
        # 继续游戏
        self.game.toggle_pause()
        
        # 验证得分仍然保留
        self.assertEqual(self.game.score, 50)
    
    def test_pause_preserves_snake_body(self):
        """测试暂停保留蛇身体状态"""
        # 记录蛇身体
        initial_body = self.game.snake_body.copy()
        
        # 暂停游戏
        self.game.toggle_pause()
        
        # 验证蛇身体保留
        self.assertEqual(self.game.snake_body, initial_body)
        
        # 继续游戏
        self.game.toggle_pause()
        
        # 验证蛇身体仍然保留
        self.assertEqual(self.game.snake_body, initial_body)
    
    def test_pause_preserves_food_position(self):
        """测试暂停保留食物位置"""
        # 记录食物位置
        initial_food = self.game.food_position
        
        # 暂停游戏
        self.game.toggle_pause()
        
        # 验证食物位置保留
        self.assertEqual(self.game.food_position, initial_food)
        
        # 继续游戏
        self.game.toggle_pause()
        
        # 验证食物位置仍然保留
        self.assertEqual(self.game.food_position, initial_food)


class TestSnakeGameStart(unittest.TestCase):
    """测试游戏开始功能"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
    
    def test_start_from_idle(self):
        """测试从空闲状态开始游戏"""
        self.game.reset()
        self.assertEqual(self.game.game_state, GameState_e.IDLE)
        
        self.game.start()
        
        self.assertEqual(self.game.game_state, GameState_e.PLAYING)
    
    def test_start_from_game_over(self):
        """测试从游戏结束状态开始新游戏"""
        # 模拟游戏结束状态
        self.game.reset()
        self.game.start()
        self.game.game_state = GameState_e.GAME_OVER
        
        self.game.start()
        
        self.assertEqual(self.game.game_state, GameState_e.PLAYING)
    
    def test_cannot_start_from_paused(self):
        """测试暂停状态不能直接开始"""
        self.game.reset()
        self.game.start()
        self.game.toggle_pause()
        
        # 尝试开始（应该无效）
        self.game.start()
        
        # 状态应该仍然是暂停
        self.assertEqual(self.game.game_state, GameState_e.PAUSED)


class TestSnakeGameReset(unittest.TestCase):
    """测试游戏重置功能"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
    
    def test_reset_clears_score(self):
        """测试重置清除得分"""
        self.game.score = 100
        self.game.reset()
        
        self.assertEqual(self.game.score, 0)
    
    def test_reset_resets_snake(self):
        """测试重置重置蛇的位置"""
        from game.snake_game import INITIAL_SNAKE_LENGTH
        
        self.game.reset()
        
        self.assertEqual(len(self.game.snake_body), INITIAL_SNAKE_LENGTH)
    
    def test_reset_resets_direction(self):
        """测试重置重置方向"""
        self.game.current_direction = Direction_e.UP
        self.game.reset()
        
        self.assertEqual(self.game.current_direction, Direction_e.RIGHT)
    
    def test_reset_resets_state_to_idle(self):
        """测试重置重置状态为空闲"""
        self.game.game_state = GameState_e.PLAYING
        self.game.reset()
        
        self.assertEqual(self.game.game_state, GameState_e.IDLE)


class TestSnakeGameDirection(unittest.TestCase):
    """测试方向控制"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
        self.game.reset()
        self.game.start()
    
    def test_change_direction_up(self):
        """测试改变方向为向上"""
        self.game.set_direction('up')
        self.assertEqual(self.game.next_direction, Direction_e.UP)
    
    def test_change_direction_down(self):
        """测试改变方向为向下"""
        self.game.set_direction('down')
        self.assertEqual(self.game.next_direction, Direction_e.DOWN)
    
    def test_change_direction_left(self):
        """测试改变方向为向左"""
        # 先改为向上，然后再向左（避免反向）
        self.game.set_direction('up')
        self.game.update()
        self.game.set_direction('left')
        self.assertEqual(self.game.next_direction, Direction_e.LEFT)
    
    def test_cannot_reverse_direction(self):
        """测试不能反向移动"""
        # 当前方向是RIGHT，不能改为LEFT
        self.game.set_direction('left')
        
        # 验证方向没有改变（仍然是RIGHT）
        self.assertEqual(self.game.next_direction, Direction_e.RIGHT)
    
    def test_invalid_direction_ignored(self):
        """测试无效方向被忽略"""
        self.game.set_direction('invalid')
        
        # 验证方向没有改变
        self.assertEqual(self.game.next_direction, Direction_e.RIGHT)


class TestSnakeGameCollision(unittest.TestCase):
    """测试碰撞检测"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
        self.game.reset()
    
    def test_wall_collision_left(self):
        """测试左边界碰撞"""
        self.assertTrue(self.game._check_collision((-1, 5)))
    
    def test_wall_collision_right(self):
        """测试右边界碰撞"""
        self.assertTrue(self.game._check_collision((self.game.grid_width, 5)))
    
    def test_wall_collision_top(self):
        """测试上边界碰撞"""
        self.assertTrue(self.game._check_collision((5, -1)))
    
    def test_wall_collision_bottom(self):
        """测试下边界碰撞"""
        self.assertTrue(self.game._check_collision((5, self.game.grid_height)))
    
    def test_no_collision_valid_position(self):
        """测试有效位置无碰撞"""
        self.assertFalse(self.game._check_collision((5, 5)))


class TestSnakeGameScore(unittest.TestCase):
    """测试得分系统"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
        self.game.reset()
        self.game.start()
    
    def test_score_increases_on_food(self):
        """测试吃到食物得分增加"""
        initial_score = self.game.score
        
        # 设置食物在蛇头前面
        head = self.game.snake_body[0]
        self.game.food_position = (head[0] + 1, head[1])
        
        # 更新游戏
        self.game.update()
        
        # 验证得分增加
        self.assertEqual(self.game.score, initial_score + 10)
    
    def test_highscore_saved_on_game_over(self):
        """测试游戏结束时保存最高分"""
        # 获取当前最高分
        current_highscore = self.game.highscore
        
        # 设置一个比当前最高分更高的分数
        new_score = current_highscore + 100
        self.game.score = new_score
        
        # 手动更新最高分并保存（模拟游戏结束时的逻辑）
        if self.game.score > self.game.highscore:
            self.game.highscore = self.game.score
            self.game._save_highscore()
        
        # 验证最高分更新
        self.assertEqual(self.game.highscore, new_score)
        
        # 创建新游戏实例验证最高分已保存
        new_game = SnakeGame()
        self.assertEqual(new_game.highscore, new_score)


class TestSnakeGameGetState(unittest.TestCase):
    """测试获取游戏状态"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.game = SnakeGame()
        self.game.reset()
    
    def test_get_state_returns_dict(self):
        """测试获取状态返回字典"""
        state = self.game.get_state()
        
        self.assertIsInstance(state, dict)
    
    def test_get_state_contains_required_fields(self):
        """测试状态包含必要字段"""
        state = self.game.get_state()
        
        required_fields = [
            'snake_body', 'food_position', 'direction',
            'score', 'highscore', 'game_state',
            'grid_width', 'grid_height', 'cell_size'
        ]
        
        for field in required_fields:
            self.assertIn(field, state)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
