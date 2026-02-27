import random
from typing import Dict
from app.schemas.requirement import EvaluationScore

class AIEvaluationService:
    """AI 评估服务 - Mock 版本"""

    def __init__(self):
        # 各维度权重配置
        self.weights = {
            "business_value": 0.30,
            "user_impact": 0.25,
            "cost": 0.20,
            "urgency": 0.15,
            "competitor": 0.10
        }

    def evaluate_requirement(self, requirement_data: Dict) -> EvaluationScore:
        """
        评估需求价值
        Mock 版本：基于规则生成评分
        """
        # 1. 商业价值评分
        business_value_score = self._evaluate_business_value(requirement_data)

        # 2. 用户影响评分
        user_impact_score = self._evaluate_user_impact(requirement_data)

        # 3. 成本评分（成本越低分数越高）
        cost_score = self._evaluate_cost(requirement_data)

        # 4. 紧急程度评分
        urgency_score = self._evaluate_urgency(requirement_data)

        # 5. 竞品对比评分
        competitor_score = self._evaluate_competitor(requirement_data)

        # 6. 计算综合得分
        total_score = (
            business_value_score * self.weights["business_value"] +
            user_impact_score * self.weights["user_impact"] +
            cost_score * self.weights["cost"] +
            urgency_score * self.weights["urgency"] +
            competitor_score * self.weights["competitor"]
        )

        # 7. 生成推荐理由
        ai_recommendation = self._generate_recommendation(
            total_score,
            business_value_score,
            user_impact_score,
            cost_score,
            urgency_score,
            competitor_score,
            requirement_data
        )

        return EvaluationScore(
            business_value_score=round(business_value_score, 2),
            user_impact_score=round(user_impact_score, 2),
            cost_score=round(cost_score, 2),
            urgency_score=round(urgency_score, 2),
            competitor_score=round(competitor_score, 2),
            total_score=round(total_score, 2),
            ai_recommendation=ai_recommendation
        )

    def _evaluate_business_value(self, data: Dict) -> float:
        """评估商业价值"""
        score = 50.0  # 基础分

        # 根据预期收益内容长度和关键词评分
        expected_benefit = data.get("expected_benefit", "")
        if expected_benefit:
            score += min(len(expected_benefit) / 20, 20)  # 最多加20分

            # 关键词加分
            keywords = ["收入", "营收", "利润", "市场份额", "转化率", "留存", "GMV"]
            for keyword in keywords:
                if keyword in expected_benefit:
                    score += 5

        # 业务背景加分
        if data.get("business_background"):
            score += 10

        return min(score, 100)

    def _evaluate_user_impact(self, data: Dict) -> float:
        """评估用户影响"""
        score = 40.0

        # 影响用户数评分
        affected_users = data.get("affected_user_count", 0)
        if affected_users:
            if affected_users > 100000:
                score += 40
            elif affected_users > 10000:
                score += 30
            elif affected_users > 1000:
                score += 20
            else:
                score += 10

        # 目标用户描述加分
        if data.get("target_users"):
            score += 15

        return min(score, 100)

    def _evaluate_cost(self, data: Dict) -> float:
        """评估实现成本（成本越低分数越高）"""
        score = 70.0

        cost_str = data.get("implementation_cost", "").lower()

        if "高" in cost_str or "复杂" in cost_str or "困难" in cost_str:
            score -= 30
        elif "中" in cost_str or "适中" in cost_str:
            score -= 15
        elif "低" in cost_str or "简单" in cost_str or "容易" in cost_str:
            score += 10

        return max(min(score, 100), 0)

    def _evaluate_urgency(self, data: Dict) -> float:
        """评估紧急程度"""
        urgency_level = data.get("urgency_level", 3)

        # 紧急程度 1-5 映射到 20-100 分
        score = 20 + (urgency_level - 1) * 20

        return score

    def _evaluate_competitor(self, data: Dict) -> float:
        """评估竞品对比"""
        score = 50.0

        competitor_info = data.get("competitor_info", "")

        if not competitor_info:
            return score

        # 关键词分析
        if "领先" in competitor_info or "超越" in competitor_info:
            score += 30
        elif "对齐" in competitor_info or "追平" in competitor_info:
            score += 20
        elif "落后" in competitor_info or "缺失" in competitor_info:
            score += 40  # 竞品有我们没有，优先级更高

        return min(score, 100)

    def _generate_recommendation(
        self,
        total_score: float,
        business_value: float,
        user_impact: float,
        cost: float,
        urgency: float,
        competitor: float,
        data: Dict
    ) -> str:
        """生成推荐理由"""

        # 优先级判断
        if total_score >= 80:
            priority = "高优先级"
            action = "强烈建议立即启动"
        elif total_score >= 60:
            priority = "中优先级"
            action = "建议近期排期"
        else:
            priority = "低优先级"
            action = "可延后处理"

        # 找出最高分维度
        scores = {
            "商业价值": business_value,
            "用户影响": user_impact,
            "实现成本": cost,
            "紧急程度": urgency,
            "竞品对比": competitor
        }
        max_dimension = max(scores, key=scores.get)

        recommendation = f"【{priority}】综合评分 {total_score:.1f} 分，{action}。\n\n"
        recommendation += f"核心优势：{max_dimension}得分最高（{scores[max_dimension]:.1f}分）。\n\n"

        # 详细分析
        if business_value >= 70:
            recommendation += "✓ 商业价值显著，预期能带来可观收益。\n"
        if user_impact >= 70:
            recommendation += "✓ 用户影响面广，能提升大量用户体验。\n"
        if cost >= 70:
            recommendation += "✓ 实现成本较低，投入产出比高。\n"
        if urgency >= 70:
            recommendation += "✓ 紧急程度高，需要优先处理。\n"
        if competitor >= 70:
            recommendation += "✓ ���品对比有优势，有助于提升竞争力。\n"

        # 风险提示
        if cost < 50:
            recommendation += "\n⚠ 注意：实现成本较高，需评估资源投入。"
        if user_impact < 50:
            recommendation += "\n⚠ 注意：用户影响面有��，需权衡优先级。"

        return recommendation


# 全局实例
ai_service = AIEvaluationService()
