#!/usr/bin/env python3
"""
需求价值评估系统 - 测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ai_evaluation import ai_service

def test_evaluation():
    """测试 AI 评估功能"""

    print("=" * 60)
    print("需求价值评估系统 - 功能测试")
    print("=" * 60)
    print()

    # 测试用例 1: 高价值需求
    print("【测试用例 1】高价值需求")
    print("-" * 60)

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

    result1 = ai_service.evaluate_requirement(requirement1)
    print(f"综合得分: {result1.total_score}")
    print(f"商业价值: {result1.business_value_score}")
    print(f"用户影响: {result1.user_impact_score}")
    print(f"实现成本: {result1.cost_score}")
    print(f"紧急程度: {result1.urgency_score}")
    print(f"竞品对比: {result1.competitor_score}")
    print(f"\nAI 推荐:\n{result1.ai_recommendation}")
    print()

    # 测试用例 2: 低价值需求
    print("【测试用例 2】低价值需求")
    print("-" * 60)

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

    result2 = ai_service.evaluate_requirement(requirement2)
    print(f"综合得分: {result2.total_score}")
    print(f"商业价值: {result2.business_value_score}")
    print(f"用户影响: {result2.user_impact_score}")
    print(f"实现成本: {result2.cost_score}")
    print(f"紧急程度: {result2.urgency_score}")
    print(f"竞品对比: {result2.competitor_score}")
    print(f"\nAI 推荐:\n{result2.ai_recommendation}")
    print()

    # 测试用例 3: 中等价值需求
    print("【测试用例 3】中等价值需求")
    print("-" * 60)

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

    result3 = ai_service.evaluate_requirement(requirement3)
    print(f"综合得分: {result3.total_score}")
    print(f"商业价值: {result3.business_value_score}")
    print(f"用户影响: {result3.user_impact_score}")
    print(f"实现成本: {result3.cost_score}")
    print(f"紧急程度: {result3.urgency_score}")
    print(f"竞品对比: {result3.competitor_score}")
    print(f"\nAI 推荐:\n{result3.ai_recommendation}")
    print()

    print("=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_evaluation()
