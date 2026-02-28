from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.requirement import RequirementStatus, RequirementType

class RequirementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    type: RequirementType
    business_background: Optional[str] = None
    expected_benefit: Optional[str] = None
    implementation_cost: Optional[str] = None  # 改为手动输入

class RequirementCreate(RequirementBase):
    pass

class RequirementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RequirementStatus] = None
    business_background: Optional[str] = None
    expected_benefit: Optional[str] = None
    implementation_cost: Optional[str] = None

class EvaluationScore(BaseModel):
    # 新的评估维度
    universality_score: float = 0  # 普适性得分
    competitor_score: float = 0     # 竞品对比得分  
    revenue_score: float = 0       # 收益潜力得分
    total_score: float = 0         # 综合得分
    ai_recommendation: str = ""    # AI 评估建议

class RequirementResponse(RequirementBase):
    id: int
    status: RequirementStatus
    universality_score: float
    competitor_score: float
    revenue_score: float
    total_score: float
    ai_recommendation: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
