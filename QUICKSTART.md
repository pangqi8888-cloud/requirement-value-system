# 需求价值评估系统 - 快速开始指南

## 项目概述

这是一个完整的需求价值评估系统 MVP，包含：
- ✅ 后端 API（FastAPI + SQLite）
- ✅ 前端界面（React + Ant Design）
- ✅ AI 评估算法（Mock 版本，基于规则）
- ✅ 可视化展示（雷达图、评分卡片）
- ✅ 智能排序和推荐

## 快速启动（3 步）

### 方式一：自动启动（推荐）

```bash
cd requirement-value-system
./start.sh
```

启动脚本会自动：
1. 检查环境
2. 安装依赖
3. 启动后端和前端服务

### 方式二：手动启动

#### 1. 启动后端

```bash
cd requirement-value-system/backend

# 创建虚拟环境（首次运行）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务：http://localhost:8000
API 文档：http://localhost:8000/docs

#### 2. 启动前端（新终端）

```bash
cd requirement-value-system/frontend

# 安装依赖（首次运行）
npm install

# 启动服务
npm run dev
```

前端服务：http://localhost:5173

## 使用指南

### 1. 创建需求

1. 打开 http://localhost:5173
2. 点击右上角"创建需求"按钮
3. 填写需求信息：
   - **基本信息**：标题、类型、描述
   - **业务信息**：业务背景、目标用户、预期收益
   - **评估维度**：影响用户数、实现成本、紧急程度、竞品信息
4. 点击"创建并评估"

### 2. 查看评估结果

系统会自动进行 AI 评估，显示：
- **综合得分**（0-100 分）
- **优先级标签**（高/中/低）
- **五维雷达图**：商业价值、用户影响、实现成本、紧急程度、竞品对比
- **AI 推荐理由**：详细的评估分析和建议

### 3. 需求排序

- 默认按综合得分降序排列
- 可切换排序方式：综合得分 / 创建时间
- 可切换排序顺序：降序 / 升序

### 4. 查看详情

点击需求列表中的"查看"按钮，可以看到：
- 完整的需求信息
- 详细的评分雷达图
- AI 推荐理由

## 测试评估算法

运行测试脚本查看评估效果：

```bash
cd requirement-value-system

# 安装后端依赖（如果还没安装）
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 运行测试
cd ..
python3 test_evaluation.py
```

测试脚本会评估 3 个不同价值的需求示例。

## 评分规则说明

### 评分维度和权重

| 维度 | 权重 | 说明 |
|------|------|------|
| 商业价值 | 30% | 预期收益、市场影响、业务背景 |
| 用户影响 | 25% | 影响用户数、用户体验提升 |
| 实现成本 | 20% | 开发工作量、技术难度（成本越低分数越高）|
| 紧急程度 | 15% | 时间敏感性、是否阻塞其他工作 |
| 竞品对比 | 10% | 竞品功能对比、竞争优势 |

### 优先级划分

- **高优先级**：综合得分 ≥ 80 分
- **中优先级**：综合得分 60-79 分
- **低优先级**：综合得分 < 60 分

## 自定义配置

### 修改评分权重

编辑 `backend/app/services/ai_evaluation.py`：

```python
self.weights = {
    "business_value": 0.30,  # 调整商业价值权重
    "user_impact": 0.25,     # 调整用户影响权重
    "cost": 0.20,            # 调整成本权重
    "urgency": 0.15,         # 调整紧急程度权重
    "competitor": 0.10       # 调整竞品对比权重
}
```

### 修改评分规则

在 `backend/app/services/ai_evaluation.py` 中修改各维度的评分方法：
- `_evaluate_business_value()` - 商业价值评分逻辑
- `_evaluate_user_impact()` - 用户影响评分逻辑
- `_evaluate_cost()` - 成本评分逻辑
- `_evaluate_urgency()` - 紧急程度评分逻辑
- `_evaluate_competitor()` - 竞品对比评分逻辑

## 项目结构

```
requirement-value-system/
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   └── requirements.py
│   │   ├── models/            # 数据模型
│   │   │   └── requirement.py
│   │   ├─�� schemas/           # Pydantic 模型
│   │   │   └── requirement.py
│   │   ├── services/          # 业务逻辑
│   │   │   └── ai_evaluation.py  # AI 评估服务
│   │   ├── core/              # 核心配置
│   │   │   └── config.py
│   │   ├── db/                # 数据库配置
│   │   │   └── session.py
│   │   └── main.py            # 应用入口
│   └── requirements.txt       # Python 依赖
├── frontend/                  # 前端项目
│   ├── src/
│   │   ├── components/        # React 组件
│   │   │   ├── RequirementForm.jsx    # 需求表单
│   │   │   └── ScoreCard.jsx          # 评分卡片
│   │   ├── pages/             # 页面
│   │   │   └── RequirementList.jsx    # 需求列表页
│   │   ├── services/          # API 服务
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── start.sh                   # 启动脚本
├── test_evaluation.py         # 测试脚本
├── README.md                  # 详细文档
└── QUICKSTART.md             # 本文件
```

## API 接口

### 创建需求
```
POST /api/v1/requirements/
```

### 获取需求列表
```
GET /api/v1/requirements/?sort_by=total_score&order=desc
```

### 获取需求详情
```
GET /api/v1/requirements/{id}
```

### 更新需求
```
PUT /api/v1/requirements/{id}
```

### 删除需求
```
DELETE /api/v1/requirements/{id}
```

完整 API 文档：http://localhost:8000/docs

## 常见问题

### Q: 如何接入真实的 AI 服务？

A: 修改 `backend/app/services/ai_evaluation.py`，将 Mock 评估逻辑替换为 AI API 调用：

```python
import openai  # 或其他 AI SDK

def evaluate_requirement(self, requirement_data: Dict) -> EvaluationScore:
    # 构造 prompt
    prompt = f"评估以下需求的价值：{requirement_data}"

    # 调用 AI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # 解析 AI 返回结果
    # ...
```

### Q: 数据存储在哪里？

A: 当前使用 SQLite 数据库，文件位于 `backend/requirements.db`。可以修改 `backend/app/core/config.py` 切换到 PostgreSQL 或 MySQL。

### Q: 如何部署到生产环境？

A:
1. 后端：使用 Gunicorn + Nginx
2. 前端：`npm run build` 后部署静态文件
3. 数据库：切换到 PostgreSQL
4. 配置环境变量和 CORS

## 下一步

1. ✅ 体验基本功能
2. ✅ 测试评估算法
3. ⏳ 根据需要调整评分规则
4. ⏳ 接入真实 AI 服务
5. ⏳ 添加用户认证
6. ⏳ 实现竞品情报系统

## 技术支持

如有问题，请查看：
- 后端 API 文档：http://localhost:8000/docs
- 详细 README：`README.md`
- 测试脚本：`test_evaluation.py`
