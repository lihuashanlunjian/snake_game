# 🐍 贪吃蛇游戏

一个基于 Python Flask + HTML5 Canvas 开发的经典贪吃蛇游戏，支持键盘和触屏操作，具有响应式设计。

## 📖 项目概述

本项目是一个功能完整的贪吃蛇游戏应用，采用前后端分离架构：

- **后端**：Python Flask 框架，提供 RESTful API
- **前端**：HTML5 Canvas + JavaScript，实现游戏渲染和交互
- **架构**：模块化设计，游戏逻辑、用户界面、网络通信分离
- **认证**：支持用户名/邮箱登录及第三方登录（微信、QQ）

### 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.8+ | 后端开发语言 |
| Flask 2.3+ | Web 框架 |
| SQLite + SQLAlchemy | 数据库及ORM框架 |
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

### 用户认证系统

- 🔐 **用户注册/登录** - 支持用户名或邮箱登录
- 🔒 **密码安全** - SHA-256 加盐哈希存储
- 🛡️ **防暴力破解** - 登录失败锁定机制
- 💪 **密码强度检测** - 弱/中等/强/非常强四级评估
- 🔄 **密码重置** - 安全的忘记密码流程
- ☑️ **记住我** - 会话持久化功能

### 第三方登录

- 💬 **微信登录** - 支持微信开放平台OAuth2.0授权
- 🐧 **QQ登录** - 支持QQ互联平台OAuth2.0授权
- 📱 **二维码扫码** - 支持扫码授权登录
- 🔗 **一键绑定** - 第三方账号与本地账号关联

### 用户界面

- 🎨 **现代视觉设计** - 渐变背景、圆角元素、动画效果
- 📱 **移动端适配** - 触屏方向按钮，自适应布局
- 🏆 **分数显示** - 实时得分和历史最高分展示
- ⚡ **交互反馈** - 按钮点击状态、加载动画、错误提示

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

4. **配置第三方登录（可选）**

复制配置示例文件并填写实际配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置微信和QQ登录参数：

```bash
# 微信开放平台配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
WECHAT_REDIRECT_URI=http://localhost:5000/api/auth/wechat/callback

# QQ互联平台配置
QQ_APP_ID=your_qq_app_id
QQ_APP_KEY=your_qq_app_key
QQ_REDIRECT_URI=http://localhost:5000/api/auth/qq/callback
```

5. **启动服务器**

```bash
python app.py
```

6. **访问游戏**

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

### 第三方登录配置

#### 微信开放平台配置

1. 访问 [微信开放平台](https://open.weixin.qq.com/)
2. 创建网站应用并获取 AppID 和 AppSecret
3. 设置授权回调域名
4. 配置环境变量 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`

#### QQ互联平台配置

1. 访问 [QQ互联平台](https://connect.qq.com/)
2. 创建网站应用并获取 AppID 和 AppKey
3. 设置授权回调地址
4. 配置环境变量 `QQ_APP_ID` 和 `QQ_APP_KEY`

## 📁 项目结构

```
snake_game/
├── app.py                    # Flask 后端服务器
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量配置示例
├── highscore.json           # 最高分存储文件（自动生成）
├── game/                    # 游戏核心逻辑模块
│   ├── __init__.py         # 模块初始化
│   └── snake_game.py       # 贪吃蛇核心逻辑
├── auth/                    # 认证模块
│   ├── __init__.py         # 模块初始化
│   ├── auth.py             # 用户认证逻辑
│   └── social_config.py    # 第三方登录配置
├── database/                # 数据库模块
│   ├── __init__.py         # 模块初始化
│   ├── db_config.py        # 数据库配置
│   ├── models.py           # 数据模型
│   ├── auth_service.py     # 认证服务
│   ├── user_dao.py         # 用户数据访问
│   └── validators.py       # 数据验证器
├── templates/               # HTML 模板
│   ├── index.html          # 游戏主页面
│   ├── login.html          # 登录页面
│   └── register.html       # 注册页面
├── static/                  # 静态资源
│   ├── css/
│   │   ├── style.css       # 游戏样式
│   │   └── login.css       # 登录/注册样式
│   └── js/
│       ├── game.js         # 游戏交互逻辑
│       ├── login.js        # 登录页面逻辑
│       └── register.js     # 注册页面逻辑
└── tests/                   # 单元测试
    ├── __init__.py         # 测试模块初始化
    ├── test_snake_game.py  # 游戏逻辑测试
    └── test_social_login.py # 第三方登录测试
```

## 🔌 API 接口

### 游戏接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 游戏主页面 |
| `/login` | GET | 登录页面 |
| `/register` | GET | 注册页面 |
| `/api/game/start` | POST | 开始新游戏 |
| `/api/game/pause` | POST | 暂停/继续游戏 |
| `/api/game/restart` | POST | 重新开始游戏 |
| `/api/game/state` | GET | 获取游戏状态 |
| `/api/game/direction` | POST | 改变移动方向 |
| `/api/game/update` | POST | 更新游戏状态 |
| `/api/game/highscore` | GET | 获取最高分 |

### 认证接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/logout` | POST | 用户登出 |
| `/api/auth/check` | GET | 检查登录状态 |
| `/api/auth/user-info` | GET | 获取用户信息 |
| `/api/auth/change-password` | POST | 修改密码 |
| `/api/auth/forgot-password` | POST | 忘记密码 |
| `/api/auth/reset-password` | POST | 重置密码 |

### 第三方登录接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/wechat/authorize` | POST | 微信授权 |
| `/api/auth/wechat/callback` | GET | 微信回调 |
| `/api/auth/qq/authorize` | POST | QQ授权 |
| `/api/auth/qq/callback` | GET | QQ回调 |
| `/api/auth/social/config` | GET | 获取第三方登录配置状态 |
| `/api/auth/social/status` | GET | 获取社交登录状态 |

## 🧪 测试

### 运行单元测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_snake_game.py
python -m pytest tests/test_social_login.py

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
- 用户认证测试
- 第三方登录测试
- API接口测试

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
- 参数不超过 5 个，超过时使用结构体封装

## 📝 更新日志

### v1.0.3 (2026-02-17)

**第三方登录功能**
- ✅ 实现微信开放平台OAuth2.0授权登录
- ✅ 实现QQ互联平台OAuth2.0授权登录
- ✅ 添加第三方登录配置管理模块
- ✅ 支持环境变量配置AppID/AppSecret
- ✅ 实现配置状态查询接口
- ✅ 添加配置指南弹窗功能

**交互体验优化**
- ✅ 按钮点击状态反馈（颜色变化、阴影效果）
- ✅ 加载动画（spinner旋转动画）
- ✅ 防重复点击机制（3秒冷却时间）
- ✅ 错误提示处理（网络异常、授权失败等）
- ✅ 二维码弹窗显示及倒计时

**测试与质量保证**
- ✅ 新增第三方登录单元测试（39个测试用例）
- ✅ 所有测试用例通过验证

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
- 感谢微信开放平台和QQ互联平台提供的第三方登录服务

---

**开发者**: lihuashanlunjian 
**最后更新**: 2026-02-17
