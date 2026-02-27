from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.requirement import RequirementStatus, RequirementType

class RequirementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    type: RequirementType
    business_background: Optional[str] = None
    target_users: Optional[str] = None
    expected_benefit: Optional[str] = None
    affected_user_count: Optional[int] = None
    implementation_cost: Optional[str] = None
    urgency_level: Optional[int] = Field(None, ge=1, le=5)
    competitor_info: Optional[str] = None

class RequirementCreate(RequirementBase):
    pass

class RequirementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RequirementStatus] = None
    business_background: Optional[str] = None
    target_users: Optional[str] = None
    expected_benefit: Optional[str] = None
    affected_user_count: Optional[int] = None
    implementation_cost: Optional[str] = None
    urgency_level: Optional[int] = Field(None, ge=1, le=5)
    competitor_info: Optional[str] = None

class EvaluationScore(BaseModel):
    business_value_score: float
    user_impact_score: float
    cost_score: float
    urgency_score: float
    competitor_score: float
    total_score: float
    ai_recommendation: str

class RequirementResponse(RequirementBase):
    id: int
    status: RequirementStatus
    business_value_score: float
    user_impact_score: float
    cost_score: float
    urgency_score: float
    competitor_score: float
    total_score: float
    ai_recommendation: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
