# 需求价值评估系统 - 文件清单

## 📁 项目结构

```
requirement-value-system/
├── 📄 README.md                    # 详细项目文档
├── 📄 QUICKSTART.md               # 快速开始指南
├── 📄 DEMO.md                     # 演示说明文档
├── 📄 PROJECT_FILES.md            # 本文件
├── 📄 .gitignore                  # Git 忽略配置
├── 🔧 start.sh                    # 一键启动脚本
├── 🧪 test_evaluation.py          # 评估算法测试脚本
│
├── 📂 backend/                    # 后端项目（Python + FastAPI）
│   ├── 📄 requirements.txt        # Python 依赖
│   └── 📂 app/
│       ├── 📄 __init__.py
│       ├── 📄 main.py            # FastAPI 应用入口
│       │
│       ├── 📂 api/               # API 路由层
│       │   ├── 📄 __init__.py
│       │   └── 📄 requirements.py # 需求管理 API
│       │
│       ├── 📂 models/            # 数据模型层
│       │   ├── 📄 __init__.py
│       │   └── 📄 requirement.py  # 需求数据模型
│       │
│       ├── 📂 schemas/           # Pydantic 模型
│       │   ├── 📄 __init__.py
│       │   └── 📄 requirement.py  # 需求 Schema
│       │
│       ├── 📂 services/          # 业务逻辑层
│       │   ├── 📄 __init__.py
│       │   └── 📄 ai_evaluation.py # AI 评估服务 ⭐核心
│       │
│       ├── 📂 core/              # 核心配置
│       │   ├── 📄 __init__.py
│       │   └── 📄 config.py      # 应用配置
│       │
│       └── 📂 db/                # 数据库配置
│           ├── 📄 __init__.py
│           └── 📄 session.py     # 数据库会话
│
└── 📂 frontend/                  # 前端项目（React + Vite）
    ├── 📄 package.json           # Node 依赖
    ├── 📄 vite.config.js         # Vite 配置
    ├── 📄 index.html             # HTML 入口
    └── 📂 src/
        ├── 📄 main.jsx           # React 入口
        ├── 📄 App.jsx            # 根组件
        │
        ├── 📂 components/        # React 组件
        │   ├── 📄 RequirementForm.jsx  # 需求创建表单 ⭐
        │   └── 📄 ScoreCard.jsx        # 评分卡片组件 ⭐
        │
        ├── 📂 pages/             # 页面组件
        │   └── 📄 RequirementList.jsx  # 需求列表页 ⭐
        │
        └── 📂 services/          # API 服务
            └── 📄 api.js         # API 封装
```

## 🔑 核心文件说明

### 后端核心

#### 1. `backend/app/services/ai_evaluation.py` ⭐⭐⭐
**最重要的文件**，包含 AI 评估算法：
- `AIEvaluationService` 类
- 5 个评分方法：
  - `_evaluate_business_value()` - 商业价值评分
  - `_evaluate_user_impact()` - 用户影响评分
  - `_evaluate_cost()` - 成本评分
  - `_evaluate_urgency()` - 紧急程度评分
  - `_evaluate_competitor()` - 竞品对比评分
- `_generate_recommendation()` - 生成推荐理由
- 权重配置：`self.weights`

**修改这个文件可以：**
- 调整评分权重
- 修改评分规则
- 接入真实 AI API

#### 2. `backend/app/api/requirements.py`
需求管理 API 接口：
- `POST /` - 创建需求并评估
- `GET /` - 获取需求列表（支持排序）
- `GET /{id}` - 获取需求详情
- `PUT /{id}` - 更新需求并重新评估
- `DELETE /{id}` - 删除需求

#### 3. `backend/app/models/requirement.py`
需求数据模型定义：
- 基本字段：title, description, type, status
- 模版字段：business_background, target_users, expected_benefit 等
- 评分字段：business_value_score, user_impact_score 等

#### 4. `backend/app/main.py`
FastAPI 应用入口：
- 应用初始化
- CORS 配置
- 路由注册
- 数据库表创建

### 前端核心

#### 1. `frontend/src/pages/RequirementList.jsx` ⭐⭐⭐
主页面组件，包含：
- 统计卡片
- 排序控制
- 需求列表表格
- 需求详情弹窗
- 所有交互逻辑

#### 2. `frontend/src/components/RequirementForm.jsx` ⭐⭐
需求创建表单：
- 完整的表单字段
- 表单验证
- API 调用
- 成功/失败提示

#### 3. `frontend/src/components/ScoreCard.jsx` ⭐⭐
评分可视化组件：
- 综合得分展示
- 五维雷达图
- 各维度评分条形图
- AI 推荐理由展示

#### 4. `frontend/src/services/api.js`
API 服务封装：
- Axios 配置
- 所有 API 接口封装

### 配置文件

#### 1. `backend/app/core/config.py`
后端配置：
- 项目名称和版本
- 数据库 URL
- CORS 配置

#### 2. `frontend/vite.config.js`
前端配置：
- 开发服务器端口
- API 代理配置

### 脚本文件

#### 1. `start.sh`
一键启动脚本：
- 环境检查
- 依赖安装
- 启动后端和前端

#### 2. `test_evaluation.py`
评估算法测试：
- 3 个测试用例
- 验证评分逻辑

## 📊 文件统计

| 类型 | 数量 | 说明 |
|------|------|------|
| Python 文件 | 13 | 后端代码 |
| JavaScript/JSX 文件 | 7 | 前端代码 |
| 配置文件 | 5 | package.json, vite.config.js 等 |
| 文档文件 | 4 | README, QUICKSTART, DEMO, 本文件 |
| 脚本文件 | 2 | start.sh, test_evaluation.py |
| **总计** | **31** | |

## 🎯 快速定位

### 想修改评分规则？
👉 `backend/app/services/ai_evaluation.py`

### 想修改 API 接口？
👉 `backend/app/api/requirements.py`

### 想修改数据模型？
👉 `backend/app/models/requirement.py`

### 想修改前端界面？
👉 `frontend/src/pages/RequirementList.jsx`

### 想修改表单字段？
👉 `frontend/src/components/RequirementForm.jsx`

### 想修改��分展示？
👉 `frontend/src/components/ScoreCard.jsx`

### 想修改配置？
👉 `backend/app/core/config.py` 或 `frontend/vite.config.js`

## 📝 代码行数统计

```
后端 Python 代码：约 800 行
前端 JavaScript/JSX 代码：约 700 行
配置和文档：约 500 行
总计：约 2000 行
```

## 🚀 开始开发

1. **阅读文档**
   - `README.md` - 了解项目整体
   - `QUICKSTART.md` - 快速上手
   - `DEMO.md` - 功能演示

2. **启动项目**
   ```bash
   ./start.sh
   ```

3. **修改代码**
   - 后端：修改 `backend/app/` 下的文件
   - 前端：修改 `frontend/src/` 下的文件

4. **测试功能**
   - 访问 http://localhost:5173
   - 查看 API 文档 http://localhost:8000/docs

5. **运行测试**
   ```bash
   python3 test_evaluation.py
   ```

## 💡 提示

- ⭐ 标记的文件是核心文件，建议优先阅读
- 所有 `__init__.py` 文件都是空文件，用于 Python 包管理
- 前端使用 Vite 热更新，修改代码后自动刷新
- 后端使用 `--reload` 模式，修改代码后自动重启
