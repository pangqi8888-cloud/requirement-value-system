#!/bin/bash

echo "======================================"
echo "需求价值评估系统 - 启动脚本"
echo "======================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q
echo "✅ 后端依赖安装完成"
echo ""

# 安装前端依赖
echo "📦 安装前端依赖..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "✅ 前端依赖已安装"
fi
echo ""

# 启动服务
echo "======================================"
echo "🚀 启动服务"
echo "======================================"
echo ""
echo "后端 API: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo "前端页面: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动后端
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# 等待用户中断
wait

# 清理进程
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
