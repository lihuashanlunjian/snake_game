# 🐍 贪吃蛇游戏

一个基于 Python Flask + HTML5 Canvas 开发的经典贪吃蛇游戏，支持键盘和触屏操作，具有响应式设计。

## 📖 项目概述

本项目是一个功能完整的贪吃蛇游戏应用，采用前后端分离架构：

- **后端**：Python Flask 框架，提供 RESTful API
- **前端**：HTML5 Canvas + JavaScript，实现游戏渲染和交互
- **架构**：模块化设计，游戏逻辑、用户界面、网络通信分离

### 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.8+ | 后端开发语言 |
| Flask 2.3+ | Web 框架 |
| HTML5 Canvas | 游戏图形渲染 |
| CSS3 | 响应式样式设计 |
| JavaScript ES6+ | 客户端交互逻辑 |

## ✨ 功能特性

### 核心功能

- 🎮 **游戏主界面渲染** - 20×20 网格，流畅的 Canvas 绑图
- 🐍 **蛇的移动控制** - 支持方向键和 WASD 键盘操作
- 🍎 **食物生成与碰撞检测** - 随机位置生成，精确碰撞判定
- 📊 **得分计算系统** - 吃食物 +10 分，自动保存最高分
- ⏯️ **游戏控制** - 开始/暂停/重新开始功能
- 📱 **响应式设计** - 支持桌面和移动设备

### 暂停功能

- ⏸️ **快捷键暂停** - 空格键快速暂停/继续
- 🖱️ **UI按钮控制** - 暂停按钮可视化操作
- 📋 **暂停菜单** - 显示当前得分、最高分和操作选项
- ⚙️ **暂停状态管理** - 游戏状态冻结，防止误操作

### 用户界面

- 🎨 **现代视觉设计** - 渐变背景、圆角元素、动画效果
- 📱 **移动端适配** - 触屏方向按钮，自适应布局
- 🏆 **分数显示** - 实时得分和历史最高分展示

## 📦 安装指南

### 环境要求

- Python 3.8 或更高版本
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/lihuashanlunjian/snake_game.git
cd snake_game
```

2. **创建虚拟环境（推荐）**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **启动服务器**

```bash
python app.py
```

5. **访问游戏**

打开浏览器访问：`http://127.0.0.1:5000`

## 🎯 使用说明

### 游戏操作

| 操作 | 按键/方式 |
|------|----------|
| 开始游戏 | 点击"开始游戏"按钮 或 空格键 |
| 暂停/继续 | 点击"暂停"按钮 或 空格键 |
| 重新开始 | 点击"重新开始"按钮 |
| 移动方向 | ↑↓←→ 方向键 或 W/A/S/D 键 |
| 移动端控制 | 点击屏幕方向按钮 |

### 游戏规则

1. 使用方向键控制蛇的移动方向
2. 吃到红色食物得 10 分，蛇身变长
3. 撞墙或撞到自己身体游戏结束
4. 最高分会自动保存到本地文件

## ⚙️ 配置方法

### 游戏参数配置

在 `game/snake_game.py` 中可以修改以下参数：

```python
# 网格大小
GRID_WIDTH = 20      # 网格宽度（格子数）
GRID_HEIGHT = 20     # 网格高度（格子数）
CELL_SIZE = 20       # 每个格子的像素大小

# 游戏设置
INITIAL_SNAKE_LENGTH = 3   # 蛇的初始长度
GAME_SPEED = 150           # 游戏速度（毫秒）
```

### 服务器配置

在 `app.py` 中可以修改服务器配置：

```python
# 启动参数
app.run(
    debug=True,           # 调试模式
    host='0.0.0.0',      # 监听地址
    port=5000            # 端口号
)
```

## 📁 项目结构

```
snake_game/
├── app.py                    # Flask 后端服务器
├── requirements.txt          # Python 依赖
├── highscore.json           # 最高分存储文件（自动生成）
├── game/                    # 游戏核心逻辑模块
│   ├── __init__.py         # 模块初始化
│   └── snake_game.py       # 贪吃蛇核心逻辑
├── templates/               # HTML 模板
│   └── index.html          # 游戏主页面
├── static/                  # 静态资源
│   ├── css/
│   │   └── style.css       # 响应式样式
│   └── js/
│       └── game.js         # 客户端交互逻辑
└── tests/                   # 单元测试
    └── test_snake_game.py  # 游戏逻辑测试
```

## 🔌 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 游戏主页面 |
| `/api/game/start` | POST | 开始新游戏 |
| `/api/game/pause` | POST | 暂停/继续游戏 |
| `/api/game/restart` | POST | 重新开始游戏 |
| `/api/game/state` | GET | 获取游戏状态 |
| `/api/game/direction` | POST | 改变移动方向 |
| `/api/game/update` | POST | 更新游戏状态 |
| `/api/game/highscore` | GET | 获取最高分 |

## 🧪 测试

### 运行单元测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_snake_game.py

# 显示详细输出
python -m pytest tests/ -v
```

### 测试覆盖范围

- 游戏初始化测试
- 蛇的移动测试
- 碰撞检测测试
- 食物生成测试
- 得分计算测试
- 暂停功能测试

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. **Fork 项目** - 点击右上角 Fork 按钮
2. **创建分支** - `git checkout -b feature/your-feature`
3. **提交更改** - `git commit -m 'Add some feature'`
4. **推送分支** - `git push origin feature/your-feature`
5. **提交 PR** - 创建 Pull Request

### 代码规范

- Python 代码遵循 PEP 8 规范
- 使用蛇形命名法（snake_case）
- 函数添加文档字符串注释
- 保持函数长度不超过 50 行

## 📝 更新日志

### v1.0.2 (2026-02-17)

**核心架构升级**
- ✅ 实现完整的数据库用户信息管理系统
- ✅ 采用SQLite数据库替代JSON文件存储，提升数据持久化能力
- ✅ 引入Flask-SQLAlchemy ORM框架，实现数据访问层与业务逻辑层分离
- ✅ 设计并实现规范化的用户信息数据表结构

**数据库功能**
- ✅ 创建用户信息表（users），包含用户ID、用户名、密码哈希、邮箱、创建时间、最后登录时间等完整字段
- ✅ 创建密码重置令牌表（password_reset_tokens），支持安全的密码重置流程
- ✅ 实现用户信息的CRUD（创建、读取、更新、删除）操作接口
- ✅ 建立数据访问对象（DAO）模式，提供清晰的数据访问抽象层

**数据验证与安全**
- ✅ 实现用户名、邮箱、密码的完整数据验证逻辑
- ✅ 添加密码强度检测功能，支持弱/中等/强/非常强四级评估
- ✅ 实现输入数据清理机制，防止XSS跨站脚本攻击
- ✅ 使用SQLAlchemy ORM参数化查询，防止SQL注入攻击
- ✅ 密码采用SHA-256算法加盐哈希存储，确保数据安全

**数据迁移与兼容**
- ✅ 开发数据库初始化脚本，支持自动创建数据库表结构
- ✅ 实现JSON用户数据到数据库的平滑迁移功能
- ✅ 自动备份原有JSON数据文件，确保数据安全
- ✅ 成功迁移现有用户数据，保持系统向后兼容

**错误处理与日志**
- ✅ 为所有数据库操作添加完整的异常处理机制
- ✅ 集成Python logging模块，实现详细的操作日志记录
- ✅ 提供清晰的错误信息输出，便于问题排查和调试

**测试与质量保证**
- ✅ 开发完整的数据库功能测试套件
- ✅ 覆盖用户注册、登录、密码重置、防暴力破解等核心功能测试
- ✅ 所有测试用例通过验证，确保系统稳定可靠

### v1.0.1 (2026-02-17)

**用户认证系统**
- ✅ 实现完整的用户登录系统，支持用户名或邮箱登录
- ✅ 开发用户注册功能，包含数据验证和重复检测
- ✅ 构建登录验证机制，保护游戏API访问安全
- ✅ 采用密码加密存储技术，保护用户敏感信息
- ✅ 实现防暴力破解保护，限制登录尝试次数并锁定账户
- ✅ 添加"记住我"功能，支持会话持久化
- ✅ 开发密码强度检测功能，引导用户设置安全密码
- ✅ 实现忘记密码功能，支持安全的密码重置流程

### v1.0.0 (2026-02-16)

**游戏核心功能**
- ✅ 实现贪吃蛇游戏核心逻辑，包含蛇的移动、食物生成、碰撞检测
- ✅ 开发暂停/继续功能，支持游戏状态管理
- ✅ 实现响应式界面设计，适配桌面和移动设备
- ✅ 添加移动端触控支持，提供虚拟方向按钮
- ✅ 实现最高分本地保存功能，持久化游戏记录
- ✅ 开发单元测试套件，确保代码质量

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

```
MIT License

Copyright (c) 2026 Snake Game Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 致谢

- 感谢 Flask 框架提供的优秀 Web 开发体验
- 感谢 HTML5 Canvas API 提供的强大图形渲染能力

---

**开发者**: lihuashanlunjian 
**最后更新**: 2026-02-16
