"""
@file    app.py
@brief   Flask后端服务器
@details 提供游戏Web服务和API接口
@author  AI Assistant
@date    2026-02-16
@version V1.0.0
"""

# 导入Flask框架的核心模块
# render_template用于渲染HTML模板
# jsonify用于返回JSON格式的响应
# request用于获取HTTP请求数据
from flask import Flask, render_template, jsonify, request

# 导入贪吃蛇游戏核心类
from game.snake_game import SnakeGame

# 创建Flask应用实例
app = Flask(__name__)

# 全局游戏实例变量，初始为None
game_instance = None


def get_game_instance():
    """
    @brief  获取游戏实例（单例模式）
    @retval SnakeGame实例对象
    """
    # 声明使用全局变量
    global game_instance
    # 如果实例不存在，则创建新实例
    if game_instance is None:
        game_instance = SnakeGame()
    # 返回游戏实例
    return game_instance


# 定义首页路由，处理GET请求
@app.route('/')
def index():
    """
    @brief  渲染游戏主页面
    @retval HTML页面内容
    """
    # 渲染并返回index.html模板
    return render_template('index.html')


# 定义开始游戏API路由，仅接受POST请求
@app.route('/api/game/start', methods=['POST'])
def start_game():
    """
    @brief  开始新游戏
    @retval JSON格式的游戏状态
    """
    # 获取游戏实例
    game = get_game_instance()
    # 重置游戏状态
    game.reset()
    # 开始游戏
    game.start()
    # 返回成功状态和当前游戏状态
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


# 定义暂停游戏API路由，仅接受POST请求
@app.route('/api/game/pause', methods=['POST'])
def pause_game():
    """
    @brief  暂停/继续游戏
    @retval JSON格式的游戏状态
    """
    # 获取游戏实例
    game = get_game_instance()
    # 切换暂停状态
    game.toggle_pause()
    # 返回成功状态和当前游戏状态
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


# 定义重新开始游戏API路由，仅接受POST请求
@app.route('/api/game/restart', methods=['POST'])
def restart_game():
    """
    @brief  重新开始游戏
    @retval JSON格式的游戏状态
    """
    # 获取游戏实例
    game = get_game_instance()
    # 重置游戏状态
    game.reset()
    # 开始游戏
    game.start()
    # 返回成功状态和当前游戏状态
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


# 定义获取游戏状态API路由，仅接受GET请求
@app.route('/api/game/state', methods=['GET'])
def get_state():
    """
    @brief  获取当前游戏状态
    @retval JSON格式的游戏状态
    """
    # 获取游戏实例
    game = get_game_instance()
    # 返回成功状态和当前游戏状态
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


# 定义改变方向API路由，仅接受POST请求
@app.route('/api/game/direction', methods=['POST'])
def change_direction():
    """
    @brief  改变蛇的移动方向
    @retval JSON格式的游戏状态
    """
    # 获取游戏实例
    game = get_game_instance()
    # 从请求体中解析JSON数据
    data = request.get_json()
    # 获取方向参数
    direction = data.get('direction')
    # 如果方向参数有效，则设置新方向
    if direction:
        game.set_direction(direction)
    # 返回成功状态和当前游戏状态
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


# 定义更新游戏API路由，仅接受POST请求
@app.route('/api/game/update', methods=['POST'])
def update_game():
    """
    @brief  更新游戏状态（移动蛇、检测碰撞等）
    @retval JSON格式的游戏状态
    """
    # 获取游戏实例
    game = get_game_instance()
    # 执行游戏更新逻辑
    game.update()
    # 返回成功状态和当前游戏状态
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


# 定义获取最高分API路由，仅接受GET请求
@app.route('/api/game/highscore', methods=['GET'])
def get_highscore():
    """
    @brief  获取历史最高分
    @retval JSON格式的最高分数据
    """
    # 获取游戏实例
    game = get_game_instance()
    # 返回成功状态和最高分
    return jsonify({
        'status': 'success',
        'highscore': game.get_highscore()
    })


# 程序入口点
if __name__ == '__main__':
    # 启动Flask开发服务器
    # debug=True: 开启调试模式，代码修改后自动重启
    # host='0.0.0.0': 监听所有网络接口，允许外部访问
    # port=5000: 使用5000端口
    app.run(debug=True, host='0.0.0.0', port=5000)
