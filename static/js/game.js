/**
 * @file    game.js
 * @brief   贪吃蛇游戏客户端交互逻辑
 * @details 处理用户输入、游戏渲染、与服务端通信
 * @author  AI Assistant
 * @date    2026-02-16
 * @version V1.0.0
 */

// 定义贪吃蛇游戏客户端类
class SnakeGameClient {
    // 构造函数，初始化游戏客户端
    constructor() {
        // 获取Canvas画布元素
        this.canvas = document.getElementById('game-canvas');
        // 获取Canvas 2D绑图上下文
        this.ctx = this.canvas.getContext('2d');
        // 获取游戏覆盖层元素（用于显示游戏状态提示）
        this.overlay = document.getElementById('game-overlay');
        // 获取覆盖层标题元素
        this.overlayTitle = document.getElementById('overlay-title');
        // 获取覆盖层消息元素
        this.overlayMessage = document.getElementById('overlay-message');
        // 获取当前得分显示元素
        this.scoreElement = document.getElementById('current-score');
        // 获取最高分显示元素
        this.highScoreElement = document.getElementById('high-score');
        
        // 获取开始游戏按钮元素
        this.btnStart = document.getElementById('btn-start');
        // 获取暂停游戏按钮元素
        this.btnPause = document.getElementById('btn-pause');
        // 获取重新开始按钮元素
        this.btnRestart = document.getElementById('btn-restart');
        
        // 获取暂停菜单元素
        this.pauseMenu = document.getElementById('pause-menu');
        // 获取暂停菜单中的当前得分元素
        this.pauseCurrentScore = document.getElementById('pause-current-score');
        // 获取暂停菜单中的最高分元素
        this.pauseHighScore = document.getElementById('pause-high-score');
        // 获取暂停菜单中的蛇身长度元素
        this.pauseSnakeLength = document.getElementById('pause-snake-length');
        
        // 获取暂停菜单中的继续游戏按钮
        this.btnResume = document.getElementById('btn-resume');
        // 获取暂停菜单中的重新开始按钮
        this.btnRestartPause = document.getElementById('btn-restart-pause');
        // 获取暂停菜单中的返回主菜单按钮
        this.btnMainMenu = document.getElementById('btn-main-menu');
        
        // 定义每个格子的像素大小
        this.cellSize = 20;
        // 定义网格宽度（格子数）
        this.gridWidth = 20;
        // 定义网格高度（格子数）
        this.gridHeight = 20;
        
        // 初始化游戏状态对象
        this.gameState = {
            // 蛇身体坐标数组
            snake_body: [],
            // 食物位置
            food_position: null,
            // 当前移动方向
            direction: 'right',
            // 当前得分
            score: 0,
            // 历史最高分
            highscore: 0,
            // 游戏状态（idle/playing/paused/game_over）
            game_state: 'idle',
            // 网格宽度
            grid_width: 20,
            // 网格高度
            grid_height: 20,
            // 格子大小
            cell_size: 20
        };
        
        // 游戏循环定时器ID
        this.gameLoop = null;
        // 游戏更新间隔（毫秒）
        this.updateInterval = 150;
        
        // 调用初始化方法
        this.init();
    }
    
    // 初始化方法
    init() {
        // 设置Canvas画布尺寸
        this.setupCanvas();
        // 绑定事件监听器
        this.bindEvents();
        // 加载历史最高分
        this.loadHighScore();
        // 显示初始覆盖层提示
        this.showOverlay('准备开始', '按"开始游戏"按钮或空格键开始');
    }
    
    // 设置Canvas画布尺寸
    setupCanvas() {
        // 根据网格大小计算并设置Canvas宽度
        this.canvas.width = this.gridWidth * this.cellSize;
        // 根据网格大小计算并设置Canvas高度
        this.canvas.height = this.gridHeight * this.cellSize;
    }
    
    // 绑定所有事件监听器
    bindEvents() {
        // 监听键盘按下事件
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // 绑定开始按钮点击事件
        this.btnStart.addEventListener('click', () => this.startGame());
        // 绑定暂停按钮点击事件
        this.btnPause.addEventListener('click', () => this.togglePause());
        // 绑定重新开始按钮点击事件
        this.btnRestart.addEventListener('click', () => this.restartGame());
        
        // 绑定暂停菜单中的继续游戏按钮
        this.btnResume.addEventListener('click', () => this.resumeGame());
        // 绑定暂停菜单中的重新开始按钮
        this.btnRestartPause.addEventListener('click', () => this.restartFromPause());
        // 绑定暂停菜单中的返回主菜单按钮
        this.btnMainMenu.addEventListener('click', () => this.returnToMainMenu());
        
        // 遍历所有移动端控制按钮
        document.querySelectorAll('.control-btn').forEach(btn => {
            // 为每个按钮绑定点击事件
            btn.addEventListener('click', () => {
                // 获取按钮的方向属性
                const direction = btn.dataset.direction;
                // 调用改变方向方法
                this.changeDirection(direction);
            });
        });
        
        // 监听窗口大小改变事件
        window.addEventListener('resize', () => this.handleResize());
    }
    
    // 处理键盘按下事件
    handleKeyDown(e) {
        // 定义按键到方向的映射
        const keyMap = {
            // 上箭头键映射为向上
            'ArrowUp': 'up',
            // 下箭头键映射为向下
            'ArrowDown': 'down',
            // 左箭头键映射为向左
            'ArrowLeft': 'left',
            // 右箭头键映射为向右
            'ArrowRight': 'right',
            // W键映射为向上
            'w': 'up',
            // S键映射为向下
            's': 'down',
            // A键映射为向左
            'a': 'left',
            // D键映射为向右
            'd': 'right'
        };
        
        // 如果按下的是方向键
        if (keyMap[e.key]) {
            // 阻止默认行为（防止页面滚动）
            e.preventDefault();
            // 调用改变方向方法
            this.changeDirection(keyMap[e.key]);
        }
        
        // 如果按下的是空格键
        if (e.code === 'Space') {
            // 阻止默认行为
            e.preventDefault();
            // 根据当前游戏状态决定操作
            if (this.gameState.game_state === 'idle' || this.gameState.game_state === 'game_over') {
                // 空闲或游戏结束状态时，开始游戏
                this.startGame();
            } else if (this.gameState.game_state === 'paused') {
                // 暂停状态时，继续游戏
                this.resumeGame();
            } else {
                // 游戏进行中时，暂停游戏
                this.togglePause();
            }
        }
        
        // 如果按下的是Esc键
        if (e.code === 'Escape') {
            // 阻止默认行为
            e.preventDefault();
            // 根据当前游戏状态决定操作
            if (this.gameState.game_state === 'playing') {
                // 游戏进行中时，暂停游戏
                this.togglePause();
            } else if (this.gameState.game_state === 'paused') {
                // 暂停状态时，继续游戏
                this.resumeGame();
            }
        }
    }
    
    // 异步方法：开始游戏
    async startGame() {
        try {
            // 发送POST请求到开始游戏API
            const response = await fetch('/api/game/start', { method: 'POST' });
            // 解析JSON响应
            const data = await response.json();
            
            // 如果请求成功
            if (data.status === 'success') {
                // 更新本地游戏状态
                this.gameState = data.game_state;
                // 更新UI界面
                this.updateUI();
                // 隐藏覆盖层
                this.hideOverlay();
                // 隐藏暂停菜单
                this.hidePauseMenu();
                // 启动游戏循环
                this.startGameLoop();
            }
        // 捕获错误
        } catch (error) {
            // 输出错误信息到控制台
            console.error('Failed to start game:', error);
        }
    }
    
    // 异步方法：切换暂停状态
    async togglePause() {
        try {
            // 发送POST请求到暂停游戏API
            const response = await fetch('/api/game/pause', { method: 'POST' });
            // 解析JSON响应
            const data = await response.json();
            
            // 如果请求成功
            if (data.status === 'success') {
                // 更新本地游戏状态
                this.gameState = data.game_state;
                // 更新UI界面
                this.updateUI();
                
                // 根据游戏状态执行相应操作
                if (this.gameState.game_state === 'paused') {
                    // 如果已暂停，停止游戏循环
                    this.stopGameLoop();
                    // 显示暂停菜单
                    this.showPauseMenu();
                } else if (this.gameState.game_state === 'playing') {
                    // 如果继续游戏，隐藏暂停菜单
                    this.hidePauseMenu();
                    // 重新启动游戏循环
                    this.startGameLoop();
                }
            }
        // 捕获错误
        } catch (error) {
            // 输出错误信息到控制台
            console.error('Failed to toggle pause:', error);
        }
    }
    
    // 继续游戏方法
    async resumeGame() {
        // 如果当前不是暂停状态，直接返回
        if (this.gameState.game_state !== 'paused') {
            return;
        }
        // 调用切换暂停方法继续游戏
        await this.togglePause();
    }
    
    // 从暂停菜单重新开始游戏
    async restartFromPause() {
        // 隐藏暂停菜单
        this.hidePauseMenu();
        // 停止当前游戏循环
        this.stopGameLoop();
        // 调用开始游戏方法
        await this.startGame();
    }
    
    // 返回主菜单
    returnToMainMenu() {
        // 停止游戏循环
        this.stopGameLoop();
        // 隐藏暂停菜单
        this.hidePauseMenu();
        // 重置游戏状态
        this.gameState.game_state = 'idle';
        // 更新UI界面
        this.updateUI();
        // 显示主菜单覆盖层
        this.showOverlay('准备开始', '按"开始游戏"按钮或空格键开始');
        // 清空画布
        this.clearCanvas();
    }
    
    // 异步方法：重新开始游戏
    async restartGame() {
        // 先停止当前游戏循环
        this.stopGameLoop();
        // 隐藏暂停菜单
        this.hidePauseMenu();
        // 调用开始游戏方法
        await this.startGame();
    }
    
    // 异步方法：改变蛇的移动方向
    async changeDirection(direction) {
        // 如果游戏不在进行中，忽略方向改变
        if (this.gameState.game_state !== 'playing') {
            return;
        }
        
        try {
            // 发送POST请求到改变方向API
            const response = await fetch('/api/game/direction', {
                method: 'POST',
                // 设置请求头为JSON格式
                headers: {
                    'Content-Type': 'application/json'
                },
                // 将方向数据转为JSON字符串发送
                body: JSON.stringify({ direction: direction })
            });
            // 解析JSON响应
            const data = await response.json();
            
            // 如果请求成功
            if (data.status === 'success') {
                // 更新本地游戏状态
                this.gameState = data.game_state;
            }
        // 捕获错误
        } catch (error) {
            // 输出错误信息到控制台
            console.error('Failed to change direction:', error);
        }
    }
    
    // 异步方法：更新游戏状态
    async updateGame() {
        try {
            // 发送POST请求到更新游戏API
            const response = await fetch('/api/game/update', { method: 'POST' });
            // 解析JSON响应
            const data = await response.json();
            
            // 如果请求成功
            if (data.status === 'success') {
                // 更新本地游戏状态
                this.gameState = data.game_state;
                // 更新UI界面
                this.updateUI();
                // 重新渲染游戏画面
                this.render();
                
                // 如果游戏结束
                if (this.gameState.game_state === 'game_over') {
                    // 停止游戏循环
                    this.stopGameLoop();
                    // 显示游戏结束提示
                    this.showOverlay('游戏结束', `最终得分: ${this.gameState.score}`);
                }
            }
        // 捕获错误
        } catch (error) {
            // 输出错误信息到控制台
            console.error('Failed to update game:', error);
        }
    }
    
    // 启动游戏循环
    startGameLoop() {
        // 如果已存在游戏循环，先清除
        if (this.gameLoop) {
            clearInterval(this.gameLoop);
        }
        // 设置定时器，按固定间隔更新游戏
        this.gameLoop = setInterval(() => this.updateGame(), this.updateInterval);
    }
    
    // 停止游戏循环
    stopGameLoop() {
        // 如果存在游戏循环
        if (this.gameLoop) {
            // 清除定时器
            clearInterval(this.gameLoop);
            // 重置游戏循环ID
            this.gameLoop = null;
        }
    }
    
    // 清空画布
    clearCanvas() {
        // 设置背景颜色为深黑色
        this.ctx.fillStyle = '#0a0a0a';
        // 填充整个画布
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    // 渲染游戏画面
    render() {
        // 设置背景颜色为深黑色
        this.ctx.fillStyle = '#0a0a0a';
        // 填充整个画布
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制网格线
        this.drawGrid();
        // 绘制食物
        this.drawFood();
        // 绘制蛇
        this.drawSnake();
    }
    
    // 绘制网格线
    drawGrid() {
        // 设置网格线颜色为半透明白色
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        // 设置线条宽度
        this.ctx.lineWidth = 1;
        
        // 绘制垂直网格线
        for (let x = 0; x <= this.gridWidth; x++) {
            // 开始新路径
            this.ctx.beginPath();
            // 移动到起点
            this.ctx.moveTo(x * this.cellSize, 0);
            // 画线到终点
            this.ctx.lineTo(x * this.cellSize, this.canvas.height);
            // 描边路径
            this.ctx.stroke();
        }
        
        // 绘制水平网格线
        for (let y = 0; y <= this.gridHeight; y++) {
            // 开始新路径
            this.ctx.beginPath();
            // 移动到起点
            this.ctx.moveTo(0, y * this.cellSize);
            // 画线到终点
            this.ctx.lineTo(this.canvas.width, y * this.cellSize);
            // 描边路径
            this.ctx.stroke();
        }
    }
    
    // 绘制蛇
    drawSnake() {
        // 获取蛇身体坐标数组
        const snakeBody = this.gameState.snake_body;
        
        // 遍历蛇身体的每个部分
        snakeBody.forEach((segment, index) => {
            // 计算当前部分的像素X坐标
            const x = segment[0] * this.cellSize;
            // 计算当前部分的像素Y坐标
            const y = segment[1] * this.cellSize;
            
            // 创建线性渐变填充
            const gradient = this.ctx.createLinearGradient(x, y, x + this.cellSize, y + this.cellSize);
            
            // 如果是蛇头
            if (index === 0) {
                // 蛇头使用亮绿色渐变
                gradient.addColorStop(0, '#00ff88');
                gradient.addColorStop(1, '#00cc6a');
            } else {
                // 蛇身根据位置计算透明度，越靠后越淡
                const alpha = 1 - (index / snakeBody.length) * 0.5;
                // 蛇身使用带透明度的绿色渐变
                gradient.addColorStop(0, `rgba(0, 255, 136, ${alpha})`);
                gradient.addColorStop(1, `rgba(0, 204, 106, ${alpha})`);
            }
            
            // 设置填充样式为渐变
            this.ctx.fillStyle = gradient;
            // 开始新路径
            this.ctx.beginPath();
            // 绘制圆角矩形
            this.ctx.roundRect(x + 1, y + 1, this.cellSize - 2, this.cellSize - 2, 4);
            // 填充路径
            this.ctx.fill();
            
            // 如果是蛇头，绘制眼睛
            if (index === 0) {
                this.drawSnakeHead(x, y);
            }
        });
    }
    
    // 绘制蛇头眼睛
    drawSnakeHead(x, y) {
        // 计算蛇头中心X坐标
        const centerX = x + this.cellSize / 2;
        // 计算蛇头中心Y坐标
        const centerY = y + this.cellSize / 2;
        // 眼睛半径
        const eyeRadius = 2;
        // 眼睛距中心的偏移量
        const eyeOffset = 4;
        
        // 设置眼睛颜色为黑色
        this.ctx.fillStyle = '#000';
        
        // 获取当前移动方向
        const direction = this.gameState.direction;
        // 定义两只眼睛的坐标变量
        let eye1X, eye1Y, eye2X, eye2Y;
        
        // 根据方向确定眼睛位置
        switch (direction) {
            case 'up':
                // 向上时，眼睛在上方两侧
                eye1X = centerX - eyeOffset;
                eye1Y = centerY - 2;
                eye2X = centerX + eyeOffset;
                eye2Y = centerY - 2;
                break;
            case 'down':
                // 向下时，眼睛在下方两侧
                eye1X = centerX - eyeOffset;
                eye1Y = centerY + 2;
                eye2X = centerX + eyeOffset;
                eye2Y = centerY + 2;
                break;
            case 'left':
                // 向左时，眼睛在左侧上下
                eye1X = centerX - 2;
                eye1Y = centerY - eyeOffset;
                eye2X = centerX - 2;
                eye2Y = centerY + eyeOffset;
                break;
            case 'right':
            default:
                // 向右时，眼睛在右侧上下
                eye1X = centerX + 2;
                eye1Y = centerY - eyeOffset;
                eye2X = centerX + 2;
                eye2Y = centerY + eyeOffset;
                break;
        }
        
        // 绘制第一只眼睛
        this.ctx.beginPath();
        this.ctx.arc(eye1X, eye1Y, eyeRadius, 0, Math.PI * 2);
        this.ctx.fill();
        
        // 绘制第二只眼睛
        this.ctx.beginPath();
        this.ctx.arc(eye2X, eye2Y, eyeRadius, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    // 绘制食物
    drawFood() {
        // 获取食物位置
        const food = this.gameState.food_position;
        // 如果没有食物位置，直接返回
        if (!food) return;
        
        // 计算食物的像素X坐标
        const x = food[0] * this.cellSize;
        // 计算食物的像素Y坐标
        const y = food[1] * this.cellSize;
        // 计算食物中心X坐标
        const centerX = x + this.cellSize / 2;
        // 计算食物中心Y坐标
        const centerY = y + this.cellSize / 2;
        
        // 创建径向渐变
        const gradient = this.ctx.createRadialGradient(
            centerX, centerY, 0,
            centerX, centerY, this.cellSize / 2
        );
        // 设置渐变起始颜色（亮红色）
        gradient.addColorStop(0, '#ff6b6b');
        // 设置渐变结束颜色（深红色）
        gradient.addColorStop(1, '#ee5a5a');
        
        // 设置填充样式为渐变
        this.ctx.fillStyle = gradient;
        // 开始新路径
        this.ctx.beginPath();
        // 绘制圆形食物
        this.ctx.arc(centerX, centerY, this.cellSize / 2 - 2, 0, Math.PI * 2);
        // 填充路径
        this.ctx.fill();
        
        // 绘制食物高光效果
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        // 开始新路径
        this.ctx.beginPath();
        // 绘制小圆形高光
        this.ctx.arc(centerX - 2, centerY - 2, 2, 0, Math.PI * 2);
        // 填充路径
        this.ctx.fill();
    }
    
    // 更新UI界面元素
    updateUI() {
        // 更新当前得分显示
        this.scoreElement.textContent = this.gameState.score;
        // 更新最高分显示
        this.highScoreElement.textContent = this.gameState.highscore;
        
        // 判断当前游戏状态
        const isPlaying = this.gameState.game_state === 'playing';
        const isPaused = this.gameState.game_state === 'paused';
        const isGameOver = this.gameState.game_state === 'game_over';
        
        // 根据游戏状态设置按钮可用性
        this.btnStart.disabled = isPlaying && !isPaused;
        this.btnPause.disabled = !isPlaying && !isPaused;
        this.btnRestart.disabled = !isPlaying && !isPaused && !isGameOver;
        
        // 根据暂停状态更新暂停按钮文字
        if (isPaused) {
            this.btnPause.textContent = '继续';
        } else {
            this.btnPause.textContent = '暂停';
        }
    }
    
    // 显示覆盖层
    showOverlay(title, message) {
        // 设置覆盖层标题
        this.overlayTitle.textContent = title;
        // 设置覆盖层消息
        this.overlayMessage.textContent = message;
        // 移除隐藏类，显示覆盖层
        this.overlay.classList.remove('hidden');
    }
    
    // 隐藏覆盖层
    hideOverlay() {
        // 添加隐藏类，隐藏覆盖层
        this.overlay.classList.add('hidden');
    }
    
    // 显示暂停菜单
    showPauseMenu() {
        // 更新暂停菜单中的统计信息
        this.pauseCurrentScore.textContent = this.gameState.score;
        this.pauseHighScore.textContent = this.gameState.highscore;
        this.pauseSnakeLength.textContent = this.gameState.snake_body.length;
        // 移除隐藏类，显示暂停菜单
        this.pauseMenu.classList.remove('hidden');
    }
    
    // 隐藏暂停菜单
    hidePauseMenu() {
        // 添加隐藏类，隐藏暂停菜单
        this.pauseMenu.classList.add('hidden');
    }
    
    // 异步方法：加载历史最高分
    async loadHighScore() {
        try {
            // 发送GET请求到获取最高分API
            const response = await fetch('/api/game/highscore');
            // 解析JSON响应
            const data = await response.json();
            
            // 如果请求成功
            if (data.status === 'success') {
                // 更新最高分显示
                this.highScoreElement.textContent = data.highscore;
            }
        // 捕获错误
        } catch (error) {
            // 输出错误信息到控制台
            console.error('Failed to load high score:', error);
        }
    }
    
    // 处理窗口大小改变事件
    handleResize() {
        // 重新渲染游戏画面
        this.render();
    }
}

// 当DOM加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    // 创建游戏客户端实例，启动游戏
    new SnakeGameClient();
});
