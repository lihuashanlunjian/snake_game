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
# session用于管理用户会话
# redirect用于重定向
# url_for用于生成URL
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

# 导入functools用于装饰器
from functools import wraps

# 导入贪吃蛇游戏核心类
from game.snake_game import SnakeGame

# 导入认证模块
from auth import register_user, login_user, create_reset_token, reset_password

# 创建Flask应用实例
app = Flask(__name__)

# 配置密钥用于session
app.secret_key = 'snake_game_secret_key_2026'

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


def login_required(f):
    """
    @brief  登录验证装饰器
    @details 检查用户是否已登录，未登录则返回错误或重定向
    @param  f: 被装饰的函数
    @retval 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查session中是否有用户信息
        if 'user_id' not in session:
            # 如果是API请求，返回JSON错误
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({
                    'success': False,
                    'message': '请先登录后再开始游戏',
                    'need_login': True
                }), 401
            # 如果是页面请求，重定向到登录页面
            return redirect(url_for('login_page', message='请先登录后再开始游戏'))
        # 已登录，继续执行原函数
        return f(*args, **kwargs)
    return decorated_function


# 定义首页路由，处理GET请求
@app.route('/')
def index():
    """
    @brief  渲染游戏主页面
    @retval HTML页面内容
    """
    # 渲染并返回index.html模板，传递登录状态
    return render_template('index.html', logged_in='user_id' in session)


# 定义登录页面路由，处理GET请求
@app.route('/login')
def login_page():
    """
    @brief  渲染登录页面
    @retval HTML页面内容
    """
    # 如果已登录，直接跳转到游戏主页
    if 'user_id' in session:
        return redirect(url_for('index'))
    # 获取提示消息
    message = request.args.get('message', '')
    # 渲染并返回login.html模板
    return render_template('login.html', message=message)


# 定义注册页面路由，处理GET请求
@app.route('/register')
def register_page():
    """
    @brief  渲染注册页面
    @retval HTML页面内容
    """
    # 如果已登录，直接跳转到游戏主页
    if 'user_id' in session:
        return redirect(url_for('index'))
    # 渲染并返回register.html模板
    return render_template('register.html')


# 定义用户登录API路由，仅接受POST请求
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """
    @brief  处理用户登录请求
    @retval JSON格式的登录结果
    """
    # 从请求体中解析JSON数据
    data = request.get_json()
    # 获取用户名/邮箱和密码
    identifier = data.get('username', '').strip()
    password = data.get('password', '')
    remember = data.get('remember', False)
    
    # 参数验证
    if not identifier or not password:
        return jsonify({
            'success': False,
            'message': '请输入用户名和密码'
        }), 400
    
    # 调用登录函数
    result = login_user(identifier, password)
    
    # 登录成功，设置session
    if result['success']:
        session['user_id'] = result.get('username')
        session['user_email'] = result.get('email')
        # 如果选择记住我，设置session持久化
        if remember:
            session.permanent = True
        return jsonify(result), 200
    else:
        return jsonify(result), 401


# 定义用户登出API路由，仅接受POST请求
@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """
    @brief  处理用户登出请求
    @retval JSON格式的登出结果
    """
    # 清除session
    session.clear()
    return jsonify({
        'success': True,
        'message': '已成功登出'
    }), 200


# 定义检查登录状态API路由，仅接受GET请求
@app.route('/api/auth/check', methods=['GET'])
def api_check_auth():
    """
    @brief  检查用户登录状态
    @retval JSON格式的登录状态
    """
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'username': session.get('user_id'),
            'email': session.get('user_email')
        }), 200
    else:
        return jsonify({
            'logged_in': False
        }), 200


# 定义用户注册API路由，仅接受POST请求
@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """
    @brief  处理用户注册请求
    @retval JSON格式的注册结果
    """
    # 从请求体中解析JSON数据
    data = request.get_json()
    # 获取注册信息
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # 参数验证
    if not username or not email or not password:
        return jsonify({
            'success': False,
            'message': '请填写所有必填项'
        }), 400
    
    # 调用注册函数
    result = register_user(username, email, password)
    
    # 返回结果
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


# 定义忘记密码API路由，仅接受POST请求
@app.route('/api/auth/forgot-password', methods=['POST'])
def api_forgot_password():
    """
    @brief  处理忘记密码请求
    @retval JSON格式的处理结果
    """
    # 从请求体中解析JSON数据
    data = request.get_json()
    # 获取邮箱
    email = data.get('email', '').strip()
    
    # 参数验证
    if not email:
        return jsonify({
            'success': False,
            'message': '请输入邮箱地址'
        }), 400
    
    # 调用创建重置令牌函数
    result = create_reset_token(email)
    
    # 返回结果（注意：即使用户不存在也返回成功，防止枚举攻击）
    return jsonify({
        'success': True,
        'message': '如果该邮箱已注册，重置链接已发送'
    }), 200


# 定义重置密码API路由，仅接受POST请求
@app.route('/api/auth/reset-password', methods=['POST'])
def api_reset_password():
    """
    @brief  处理重置密码请求
    @retval JSON格式的处理结果
    """
    # 从请求体中解析JSON数据
    data = request.get_json()
    # 获取令牌和新密码
    token = data.get('token', '')
    new_password = data.get('password', '')
    
    # 参数验证
    if not token or not new_password:
        return jsonify({
            'success': False,
            'message': '参数错误'
        }), 400
    
    # 调用重置密码函数
    result = reset_password(token, new_password)
    
    # 返回结果
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


# 定义开始游戏API路由，仅接受POST请求
@app.route('/api/game/start', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
