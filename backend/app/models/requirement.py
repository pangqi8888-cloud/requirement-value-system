from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class RequirementStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class RequirementType(str, enum.Enum):
    FEATURE = "feature"
    OPTIMIZATION = "optimization"
    BUG_FIX = "bug_fix"

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(SQLEnum(RequirementType), nullable=False)
    status = Column(SQLEnum(RequirementStatus), default=RequirementStatus.PENDING)

    # 需求模版字段（简化版）
    business_background = Column(Text)  # 业务背景
    expected_benefit = Column(Text)  # 预期收益
    implementation_cost = Column(String(500))  # 实现成本估算（手动输入）
    
    # 以下字段保留但新表单不再使用（兼容旧数据）
    target_users = Column(String(500))  # 目标用户
    affected_user_count = Column(Integer)  # 影响用户数
    urgency_level = Column(Integer)  # 紧急程度 1-5
    competitor_info = Column(Text)  # 竞品信息

    # AI 评估结果（新版）
    universality_score = Column(Float, default=0.0)  # 普适性得分
    competitor_score = Column(Float, default=0.0)    # 竞品对比得分
    revenue_score = Column(Float, default=0.0)       # 收益潜力得分
    total_score = Column(Float, default=0.0)         # 综合得分
    ai_recommendation = Column(Text)  # AI 评估建议

    # 旧字段保留兼容（将迁移到新字段）
    business_value_score = Column(Float, default=0.0)  # 商业价值得分
    user_impact_score = Column(Float, default=0.0)  # 用户影响得分
    cost_score = Column(Float, default=0.0)  # 成本得分
    urgency_score = Column(Float, default=0.0)  # 紧急程度得分

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
