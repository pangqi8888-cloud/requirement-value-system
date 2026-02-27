#!/usr/bin/env python3
"""
需求价值评估系统 - 简化版后端服务
使用 Python 内置库，无需安装依赖
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入评估服务
from demo import AIEvaluationService

# 全局变量
requirements_db = []
next_id = 1
ai_service = AIEvaluationService()


class RequirementHandler(BaseHTTPRequestHandler):
    """处理需求相关的 HTTP 请求"""

    def _set_headers(self, status=200):
        """设置响应���"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        """处理 OPTIONS 请求（CORS 预检）"""
        self._set_headers(200)

    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/api/v1/requirements/' or path == '/api/v1/requirements':
            # 获取需求列表
            self._set_headers(200)

            # 解析查询参数
            query_params = urllib.parse.parse_qs(parsed_path.query)
            sort_by = query_params.get('sort_by', ['total_score'])[0]
            order = query_params.get('order', ['desc'])[0]

            # 排序
            sorted_reqs = sorted(
                requirements_db,
                key=lambda x: x.get(sort_by, 0),
                reverse=(order == 'desc')
            )

            self.wfile.write(json.dumps(sorted_reqs, ensure_ascii=False).encode('utf-8'))

        elif path.startswith('/api/v1/requirements/'):
            # 获取单个需求
            req_id = int(path.split('/')[-1])
            requirement = next((r for r in requirements_db if r['id'] == req_id), None)

            if requirement:
                self._set_headers(200)
                self.wfile.write(json.dumps(requirement, ensure_ascii=False).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'detail': '需求不存在'}).encode('utf-8'))

        elif path == '/' or path == '/api/v1':
            # 根路径
            self._set_headers(200)
            response = {
                'message': '需求价值评估系统 API',
                'version': '0.1.0',
                'docs': '/docs (暂不可用，请使用前端界面)'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'detail': 'Not Found'}).encode('utf-8'))

    def do_POST(self):
        """处理 POST 请求"""
        global next_id

        if self.path == '/api/v1/requirements/' or self.path == '/api/v1/requirements':
            # 创建需求
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            requirement_data = json.loads(post_data.decode('utf-8'))

            # AI 评估
            evaluation = ai_service.evaluate_requirement(requirement_data)

            # 创建需求对象
            requirement = {
                'id': next_id,
                'title': requirement_data.get('title', ''),
                'description': requirement_data.get('description', ''),
                'type': requirement_data.get('type', 'feature'),
                'status': 'pending',
                'business_background': requirement_data.get('business_background'),
                'target_users': requirement_data.get('target_users'),
                'expected_benefit': requirement_data.get('expected_benefit'),
                'affected_user_count': requirement_data.get('affected_user_count'),
                'implementation_cost': requirement_data.get('implementation_cost'),
                'urgency_level': requirement_data.get('urgency_level'),
                'competitor_info': requirement_data.get('competitor_info'),
                'business_value_score': evaluation.business_value_score,
                'user_impact_score': evaluation.user_impact_score,
                'cost_score': evaluation.cost_score,
                'urgency_score': evaluation.urgency_score,
                'competitor_score': evaluation.competitor_score,
                'total_score': evaluation.total_score,
                'ai_recommendation': evaluation.ai_recommendation,
                'created_at': datetime.now().isoformat(),
                'updated_at': None
            }

            requirements_db.append(requirement)
            next_id += 1

            self._set_headers(201)
            self.wfile.write(json.dumps(requirement, ensure_ascii=False).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'detail': 'Not Found'}).encode('utf-8'))

    def do_DELETE(self):
        """处理 DELETE 请求"""
        if self.path.startswith('/api/v1/requirements/'):
            req_id = int(self.path.split('/')[-1])

            global requirements_db
            original_length = len(requirements_db)
            requirements_db = [r for r in requirements_db if r['id'] != req_id]

            if len(requirements_db) < original_length:
                self._set_headers(204)
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'detail': '需求不存在'}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'detail': 'Not Found'}).encode('utf-8'))

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port=8000):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequirementHandler)

    print("=" * 80)
    print("🚀 需求价值评估系统 - 后端服务")
    print("=" * 80)
    print(f"\n✅ 服务已启动: http://localhost:{port}")
    print(f"📚 API 端点: http://localhost:{port}/api/v1/requirements/")
    print(f"\n💡 提示: 请在另一个终端启动前端服务")
    print(f"   cd frontend && npm install && npm run dev")
    print(f"\n按 Ctrl+C 停止服务\n")
    print("=" * 80)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务已停止")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
