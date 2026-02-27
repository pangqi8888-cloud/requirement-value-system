# 需求价值评估系统

一个基于 AI 的需求价值评估系统，帮助产品团队科学评估和排序需求优先级。

## 功能特性

- 📝 **需求管理**：创建、编辑、删除需求
- 🤖 **AI 智能评估**：自动评估需求的商业价值、用户影响、实现成本、紧急程度和竞品对比
- 📊 **可视化展示**：雷达图、评分卡片、排序列表
- 🎯 **智能排序**：根据综合得分自动排序需求优先级
- 💡 **推荐理由**：AI 生成详细的评估理由和建议

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- SQLAlchemy
- SQLite

### 前端
- React 18
- Ant Design
- Recharts
- Axios

## 快速开始

### 1. 安装依赖

#### 后端
```bash
cd backend
pip install -r requirements.txt
```

#### 前端
```bash
cd frontend
npm install
```

### 2. 启动服务

#### 启动后端（终端 1）
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档：http://localhost:8000/docs

#### 启动前端（终端 2）
```bash
cd frontend
npm run dev
```

前端访问地址：http://localhost:5173

### 3. 使用系统

1. 打开浏览器访问 http://localhost:5173
2. 点击"创建需求"按钮
3. 填写需求信息（标题、描述、业务背景、预期收益等）
4. 提交后系统自动进行 AI 评估
5. 查看评估结果和排序建议

## 评分维度

系统从以下 5 个维度评估需求价值：

1. **商业价值**（权重 30%）
   - 预期收益
   - 市场影响
   - 业务背景

2. **用户影响**（权重 25%）
   - 影响���户数量
   - 用户体验提升

3. **实现成本**（权重 20%）
   - 开发工作量
   - 技术难度
   - 资源投入

4. **紧急程度**（权重 15%）
   - 时间敏感性
   - 是否阻塞其他工作

5. **竞品对比**（权重 10%）
   - 竞品功能对比
   - 竞争优势评估

## 项目结构

```
requirement-value-system/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务逻辑
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库配置
│   │   └── main.py         # 应用入口
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── pages/          # 页面
│   │   ├── services/       # API 服务
│   │   └── main.jsx        # 应用入口
│   └── package.json        # Node 依赖
└── README.md
```

## API 接口

### 需求管理

- `POST /api/v1/requirements/` - 创建需求
- `GET /api/v1/requirements/` - 获取需求列表
- `GET /api/v1/requirements/{id}` - 获取需求详情
- `PUT /api/v1/requirements/{id}` - 更新需求
- `DELETE /api/v1/requirements/{id}` - 删除需求

## 当前版本说明

这是一个 MVP 原型版本，使用 Mock 数据模拟 AI 评估。主要特点：

- ✅ 完整的前后端功能
- ✅ 基于规则的智能评分算法
- ✅ 可视化评分展示
- ✅ 需求排序和筛选
- ⏳ 后续可接入真实 AI 服务（OpenAI/Claude/国内大模型）

## 后续迭代计划

1. **AI 集成**
   - 接入 OpenAI/Claude API
   - 支持自定义 AI 模型

2. **竞品情报**
   - 竞品功能库管理
   - 自动爬虫抓取

3. **用户权限**
   - 用户登录认证
   - 角色权限管理

4. **需求模版**
   - 自定义需求模版
   - 动态表单配置

5. **协作功能**
   - 需求评论
   - @提醒
   - 审批流程

## 开发说明

### 修改评分权重

编辑 `backend/app/services/ai_evaluation.py` 中的 `weights` 配置：

```python
self.weights = {
    "business_value": 0.30,  # 商业价值权重
    "user_impact": 0.25,     # 用户影响权重
    "cost": 0.20,            # 成本权重
    "urgency": 0.15,         # 紧急程度权重
    "competitor": 0.10       # 竞品对比权重
}
```

### 自定义评分规则

修改 `backend/app/services/ai_evaluation.py` 中的评分方法：
- `_evaluate_business_value()` - 商业价值评分
- `_evaluate_user_impact()` - 用户影响评分
- `_evaluate_cost()` - 成本评分
- `_evaluate_urgency()` - 紧急程度评分
- `_evaluate_competitor()` - 竞品对比评分

## License

MIT
