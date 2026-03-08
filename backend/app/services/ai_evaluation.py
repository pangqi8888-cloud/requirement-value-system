import json
import os
import requests
from typing import Dict
from app.schemas.requirement import EvaluationScore

# 千问 API 配置 - 从环境变量读取
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "sk-929c71ee1b344b32a1a5373351039a34")
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
MODEL_NAME = "qwen-turbo"


class AIEvaluationService:
    """AI 评估服务 - 千问版本"""

    def __init__(self):
        pass

    def evaluate_requirement(self, requirement_data: Dict) -> EvaluationScore:
        """
        评估需求价值
        由 AI 完全自主判断：普适性、竞品对比、收益潜力
        """
        # 调用千问进行综合评估
        ai_result = self._call_qwen_evaluation(requirement_data)

        if ai_result:
            return ai_result
        else:
            # API 失败时的默认响应
            return EvaluationScore(
                universality_score=50.0,
                competitor_score=50.0,
                revenue_score=50.0,
                total_score=50.0,
                ai_recommendation="AI 评估服务暂时不可用，请稍后重试。"
            )

    def _call_qwen(self, prompt: str) -> str:
        """调用千问 API"""
        headers = {
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(
                QWEN_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"千问 API 调用失败: {e}")
            return None

    def _call_qwen_evaluation(self, data: Dict) -> EvaluationScore:
        """调用千问进行综合评估"""

        # 构建需求信息
        requirement_info = f"""
## 需求信息

**标题：** {data.get('title', '未命名')}
**类型：** {data.get('type', '未指定')}
**描述：** {data.get('description', '无')}
**业务背景：** {data.get('business_background', '无')}
**预期收益：** {data.get('expected_benefit', '无')}
**实现成本描述：** {data.get('implementation_cost', '无')}
"""

        prompt = f"""你是一个专业的需求分析和产品策略专家。请对以下需求进行深度分析评估。

{requirement_info}

## 评估要求

你需要从以下三个维度进行评估，每个维度给出 0-100 的分数：

### 1. 普适性评估 (universality_score)
分析这个需求在该场景下是否具有普适性：
- 是否是大多数用户都会用到的功能
- 是否解决了普遍存在的痛点
- 是否具有通用价值，而非小众需求

### 2. 竞品对比分析 (competitor_score)
你需要分析国内和海外 TOP3 的主流安全厂商的同类产品能力：
- **国内安全厂商**：奇安信、深信服、绿盟科技
- **海外安全厂商**：Palo Alto Networks、Fortinet、Cisco Secure

结合这些厂商的能力情况，评估我们做这个需求的价值：
- 如果竞品都没有而我们有，是领先机会
- 如果竞品都有我们需要跟进，是必要需求
- 如果竞品做得很好我们可以借鉴，是优化机会

### 3. 收益潜力评估 (revenue_score)
结合业务背景和预期收益，评估这个需求能带来的规模收益：
- 能否带来直接收入增长
- 能否提升用户留存/转化
- 能否降低运营成本
- 能否增强产品竞争力

## 输出格式

请严格按照以下 JSON 格式输出评估结果：

```json
{{
  "universality_score": 85,
  "competitor_score": 70,
  "revenue_score": 80,
  "total_score": 78,
  "recommendation": "这里是你对需求的综合评估和建议，包含：1.需求价值总结 2.优先级建议 3.实施建议 4.风险提示"
}}
```

要求：
1. total_score = (universality_score + competitor_score + revenue_score) / 3
2. recommendation 部分用中文，包含你对需求的完整分析和建议
3. 重点说明这个需求是否值得做，给出明确的优先级判断
4. 如果涉及安全厂商的竞品分析，请给出具体分析

请直接输出 JSON，不要有其他内容："""

        ai_result = self._call_qwen(prompt)
        
        if ai_result:
            try:
                # 提取 JSON
                json_start = ai_result.find('{')
                json_end = ai_result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = ai_result[json_start:json_end]
                    result = json.loads(json_str)
                    
                    return EvaluationScore(
                        universality_score=round(result.get('universality_score', 50), 2),
                        competitor_score=round(result.get('competitor_score', 50), 2),
                        revenue_score=round(result.get('revenue_score', 50), 2),
                        total_score=round(result.get('total_score', 50), 2),
                        ai_recommendation=result.get('recommendation', '评估完成')
                    )
            except Exception as e:
                print(f"解析 AI 结果失败: {e}")
                print(f"原始输出: {ai_result}")
        
        return None


# 全局实例
ai_service = AIEvaluationService()
