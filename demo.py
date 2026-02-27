#!/usr/bin/env python3
"""
需求价值评估系统 - 独立演示脚本
不需要安装任何依赖，直接展示评估算法效果
"""

from typing import Dict
from dataclasses import dataclass

@dataclass
class EvaluationScore:
    business_value_score: float
    user_impact_score: float
    cost_score: float
    urgency_score: float
    competitor_score: float
    total_score: float
    ai_recommendation: str

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
        """评估需求价值"""
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
            recommendation += "✓ 竞品对比有优势，有助于提升竞争力。\n"

        # 风险提示
        if cost < 50:
            recommendation += "\n⚠ 注意：实现成本较高，需评估资源投入。"
        if user_impact < 50:
            recommendation += "\n⚠ 注意：用户影响面有限，需权衡优先级。"

        return recommendation


def print_separator(char="=", length=80):
    print(char * length)


def print_requirement_info(title, requirement):
    """打印需求信息"""
    print(f"\n【{title}】")
    print("-" * 80)
    print(f"标题: {requirement['title']}")
    print(f"描述: {requirement['description']}")
    if requirement.get('expected_benefit'):
        print(f"预期收益: {requirement['expected_benefit']}")
    if requirement.get('affected_user_count'):
        print(f"影响用户数: {requirement['affected_user_count']:,}")
    if requirement.get('implementation_cost'):
        print(f"实现成本: {requirement['implementation_cost']}")
    if requirement.get('urgency_level'):
        print(f"紧急程度: {requirement['urgency_level']}/5")
    if requirement.get('competitor_info'):
        print(f"竞品信息: {requirement['competitor_info']}")


def print_evaluation_result(result):
    """打印评估结果"""
    print("\n" + "=" * 80)
    print("📊 AI 评估结果")
    print("=" * 80)
    print(f"\n🎯 综合得分: {result.total_score:.1f} 分")
    print("\n各维度得分:")
    print(f"  • 商业价值: {result.business_value_score:.1f} 分 (权重 30%)")
    print(f"  • 用户影响: {result.user_impact_score:.1f} 分 (权重 25%)")
    print(f"  • 实现成本: {result.cost_score:.1f} 分 (权重 20%)")
    print(f"  • 紧急程度: {result.urgency_score:.1f} 分 (权重 15%)")
    print(f"  • 竞品对比: {result.competitor_score:.1f} 分 (权重 10%)")
    print("\n💡 AI 推荐:")
    print("-" * 80)
    print(result.ai_recommendation)
    print()


def main():
    """主函数"""
    print_separator("=")
    print("🚀 需求价值评估系统 - 演示")
    print_separator("=")
    print("\n本演示展示 AI 智能评估算法的效果")
    print("系统会从 5 个维度评估需求价值，并给出综合得分和推荐建议\n")

    ai_service = AIEvaluationService()

    # 测试用例 1: 高价值需求
    requirement1 = {
        "title": "用户画像分析功能",
        "description": "为企业用户提供详细的用户画像分析，帮助精准营销",
        "type": "feature",
        "business_background": "当前缺乏用户数据分析能力，影响营销效果",
        "target_users": "企业用户、市场部门",
        "expected_benefit": "预计提升转化率 20%，增加年营收 500 万元，提高用户留存率",
        "affected_user_count": 50000,
        "implementation_cost": "中",
        "urgency_level": 4,
        "competitor_info": "主要竞品都已具备此功能，我们目前落后"
    }

    print_separator("=")
    print_requirement_info("测试用例 1: 高价值需求", requirement1)
    result1 = ai_service.evaluate_requirement(requirement1)
    print_evaluation_result(result1)

    # 测试用例 2: 低价值需求
    requirement2 = {
        "title": "修改按钮颜色",
        "description": "将登录按钮颜色从蓝色改为绿色",
        "type": "optimization",
        "business_background": "",
        "target_users": "所有用户",
        "expected_benefit": "界面更美观",
        "affected_user_count": 1000,
        "implementation_cost": "低",
        "urgency_level": 1,
        "competitor_info": ""
    }

    print_separator("=")
    print_requirement_info("测试用例 2: 低价值需求", requirement2)
    result2 = ai_service.evaluate_requirement(requirement2)
    print_evaluation_result(result2)

    # 测试用例 3: 中等价值需求
    requirement3 = {
        "title": "导出 Excel 功能",
        "description": "支持将数据报表导出为 Excel 文件",
        "type": "feature",
        "business_background": "用户经常需要下载数据进行二次分析",
        "target_users": "企业用户",
        "expected_benefit": "提升用户体验，减少客服咨询",
        "affected_user_count": 10000,
        "implementation_cost": "低",
        "urgency_level": 3,
        "competitor_info": "竞品已有此功能，我们需要对齐"
    }

    print_separator("=")
    print_requirement_info("测试用例 3: 中等价值需求", requirement3)
    result3 = ai_service.evaluate_requirement(requirement3)
    print_evaluation_result(result3)

    # 排序展示
    print_separator("=")
    print("📋 需求优先级排序")
    print_separator("=")
    print("\n根据综合得分排序（从高到低）:\n")

    requirements = [
        (requirement1['title'], result1.total_score),
        (requirement2['title'], result2.total_score),
        (requirement3['title'], result3.total_score),
    ]
    requirements.sort(key=lambda x: x[1], reverse=True)

    for i, (title, score) in enumerate(requirements, 1):
        priority = "🔴 高" if score >= 80 else "🟡 中" if score >= 60 else "⚪ 低"
        print(f"#{i}  {priority}  {score:.1f} 分  {title}")

    print_separator("=")
    print("\n✅ 演示完成！")
    print("\n💡 说明:")
    print("  • 综合得分 ≥ 80 分: 高优先级（强烈建议立即启动）")
    print("  • 综合得分 60-79 分: 中优先级（建议近期排期）")
    print("  • 综合得分 < 60 分: 低优先级（可延后处理）")
    print("\n📚 完整系统包含:")
    print("  • Web 界面（React + Ant Design）")
    print("  • RESTful API（FastAPI）")
    print("  • 数据库存储（SQLite）")
    print("  • 可视化图表（雷达图、评分卡片）")
    print("\n🚀 启动完整系统:")
    print("  cd requirement-value-system")
    print("  ./start.sh")
    print_separator("=")


if __name__ == "__main__":
    main()
