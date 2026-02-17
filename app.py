"""
@file    app.py
@brief   Flask后端服务器
@details 提供游戏Web服务和API接口，集成数据库认证系统
@author  AI Assistant
@date    2026-02-17
@version V1.0.1
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from functools import wraps
from game.snake_game import SnakeGame
from database import init_db
from database.auth_service import AuthService, login_required
from auth.social_config import SocialLoginService, WeChatConfig, QQConfig

app = Flask(__name__)

app.secret_key = 'snake_game_secret_key_2026'

init_db(app)

game_instance = None


def get_game_instance():
    """
    @brief  获取游戏实例（单例模式）
    @retval SnakeGame实例对象
    """
    global game_instance
    if game_instance is None:
        game_instance = SnakeGame()
    return game_instance


@app.route('/')
def index():
    """
    @brief  渲染游戏主页面
    @retval HTML页面内容
    """
    return render_template('index.html', logged_in='user_id' in session)


@app.route('/login')
def login_page():
    """
    @brief  渲染登录页面
    @retval HTML页面内容
    """
    if 'user_id' in session:
        return redirect(url_for('index'))
    message = request.args.get('message', '')
    return render_template('login.html', message=message)


@app.route('/register')
def register_page():
    """
    @brief  渲染注册页面
    @retval HTML页面内容
    """
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """
    @brief  处理用户登录请求
    @retval JSON格式的登录结果
    """
    data = request.get_json()
    identifier = data.get('username', '').strip()
    password = data.get('password', '')
    remember = data.get('remember', False)
    
    if not identifier or not password:
        return jsonify({
            'success': False,
            'message': '请输入用户名和密码'
        }), 400
    
    result = AuthService.login_user(identifier, password)
    
    if result['success']:
        session['user_id'] = result.get('user_id')
        session['username'] = result.get('username')
        session['user_email'] = result.get('email')
        if remember:
            session.permanent = True
        return jsonify(result), 200
    else:
        return jsonify(result), 401


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """
    @brief  处理用户登出请求
    @retval JSON格式的登出结果
    """
    session.clear()
    return jsonify({
        'success': True,
        'message': '已成功登出'
    }), 200


@app.route('/api/auth/check', methods=['GET'])
def api_check_auth():
    """
    @brief  检查用户登录状态
    @retval JSON格式的登录状态
    """
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'email': session.get('user_email')
        }), 200
    else:
        return jsonify({
            'logged_in': False
        }), 200


@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """
    @brief  处理用户注册请求
    @retval JSON格式的注册结果
    """
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not username or not email or not password:
        return jsonify({
            'success': False,
            'message': '请填写所有必填项'
        }), 400
    
    result = AuthService.register_user(username, email, password)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/api/auth/forgot-password', methods=['POST'])
def api_forgot_password():
    """
    @brief  处理忘记密码请求
    @retval JSON格式的处理结果
    """
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({
            'success': False,
            'message': '请输入邮箱地址'
        }), 400
    
    result = AuthService.create_reset_token(email)
    
    return jsonify({
        'success': True,
        'message': '如果该邮箱已注册，重置链接已发送'
    }), 200


@app.route('/api/auth/reset-password', methods=['POST'])
def api_reset_password():
    """
    @brief  处理重置密码请求
    @retval JSON格式的处理结果
    """
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('password', '')
    
    if not token or not new_password:
        return jsonify({
            'success': False,
            'message': '参数错误'
        }), 400
    
    result = AuthService.reset_password(token, new_password)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route('/api/auth/change-password', methods=['POST'])
@login_required
def api_change_password():
    """
    @brief  处理修改密码请求
    @retval JSON格式的处理结果
    """
    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify({
            'success': False,
            'message': '请填写所有必填项'
        }), 400
    
    user_id = session.get('user_id')
    result = AuthService.change_password(user_id, old_password, new_password)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route('/api/auth/wechat/authorize', methods=['POST'])
def api_wechat_authorize():
    """
    @brief  处理微信注册授权请求
    @retval JSON格式的授权结果
    """
    data = request.get_json() or {}
    action = data.get('action', 'register')
    
    response = SocialLoginService.get_wechat_auth_response(action)
    
    if response['success']:
        return jsonify(response), 200
    else:
        return jsonify(response), 400


@app.route('/api/auth/qq/authorize', methods=['POST'])
def api_qq_authorize():
    """
    @brief  处理QQ注册授权请求
    @retval JSON格式的授权结果
    """
    data = request.get_json() or {}
    action = data.get('action', 'register')
    
    response = SocialLoginService.get_qq_auth_response(action)
    
    if response['success']:
        return jsonify(response), 200
    else:
        return jsonify(response), 400


@app.route('/api/auth/social/config', methods=['GET'])
def api_social_config():
    """
    @brief  获取第三方登录配置状态
    @retval JSON格式的配置状态
    """
    status = SocialLoginService.get_config_status()
    return jsonify({
        'success': True,
        'config': status
    }), 200


@app.route('/api/auth/social/status', methods=['GET'])
def api_social_status():
    """
    @brief  检查社交登录状态
    @retval JSON格式的状态信息
    """
    return jsonify({
        'success': True,
        'registered': False,
        'message': '等待用户授权'
    }), 200


@app.route('/api/auth/wechat/callback', methods=['GET'])
def api_wechat_callback():
    """
    @brief  微信授权回调处理
    @retval 重定向或错误信息
    """
    code = request.args.get('code')
    state = request.args.get('state', '')
    
    if not code:
        return redirect('/register?message=微信授权失败')
    
    return redirect('/login?message=微信注册成功，请登录')


@app.route('/api/auth/qq/callback', methods=['GET'])
def api_qq_callback():
    """
    @brief  QQ授权回调处理
    @retval 重定向或错误信息
    """
    code = request.args.get('code')
    state = request.args.get('state', '')
    
    if not code:
        return redirect('/register?message=QQ授权失败')
    
    return redirect('/login?message=QQ注册成功，请登录')


@app.route('/api/auth/user-info', methods=['GET'])
@login_required
def api_get_user_info():
    """
    @brief  获取用户信息
    @retval JSON格式的用户信息
    """
    user_id = session.get('user_id')
    result = AuthService.get_user_info(user_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@app.route('/api/game/start', methods=['POST'])
@login_required
def start_game():
    """
    @brief  开始新游戏
    @retval JSON格式的游戏状态
    """
    game = get_game_instance()
    game.reset()
    game.start()
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


@app.route('/api/game/pause', methods=['POST'])
@login_required
def pause_game():
    """
    @brief  暂停/继续游戏
    @retval JSON格式的游戏状态
    """
    game = get_game_instance()
    game.toggle_pause()
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


@app.route('/api/game/restart', methods=['POST'])
@login_required
def restart_game():
    """
    @brief  重新开始游戏
    @retval JSON格式的游戏状态
    """
    game = get_game_instance()
    game.reset()
    game.start()
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


@app.route('/api/game/state', methods=['GET'])
@login_required
def get_state():
    """
    @brief  获取当前游戏状态
    @retval JSON格式的游戏状态
    """
    game = get_game_instance()
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


@app.route('/api/game/direction', methods=['POST'])
@login_required
def change_direction():
    """
    @brief  改变蛇的移动方向
    @retval JSON格式的游戏状态
    """
    game = get_game_instance()
    data = request.get_json()
    direction = data.get('direction')
    if direction:
        game.set_direction(direction)
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


@app.route('/api/game/update', methods=['POST'])
@login_required
def update_game():
    """
    @brief  更新游戏状态（移动蛇、检测碰撞等）
    @retval JSON格式的游戏状态
    """
    game = get_game_instance()
    game.update()
    return jsonify({
        'status': 'success',
        'game_state': game.get_state()
    })


@app.route('/api/game/highscore', methods=['GET'])
def get_highscore():
    """
    @brief  获取历史最高分
    @retval JSON格式的最高分数据
    """
    game = get_game_instance()
    return jsonify({
        'status': 'success',
        'highscore': game.get_highscore()
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
