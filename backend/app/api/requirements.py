from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.requirement import Requirement
from app.schemas.requirement import RequirementCreate, RequirementResponse, RequirementUpdate
from app.services.ai_evaluation import ai_service

router = APIRouter()

@router.post("/", response_model=RequirementResponse, status_code=201)
def create_requirement(
    requirement: RequirementCreate,
    db: Session = Depends(get_db)
):
    """创建需求并进行 AI 评估"""

    # 1. 创建需求对象
    db_requirement = Requirement(**requirement.model_dump())

    # 2. AI 评估
    evaluation = ai_service.evaluate_requirement(requirement.model_dump())

    # 3. 保存评估结果
    db_requirement.business_value_score = evaluation.business_value_score
    db_requirement.user_impact_score = evaluation.user_impact_score
    db_requirement.cost_score = evaluation.cost_score
    db_requirement.urgency_score = evaluation.urgency_score
    db_requirement.competitor_score = evaluation.competitor_score
    db_requirement.total_score = evaluation.total_score
    db_requirement.ai_recommendation = evaluation.ai_recommendation

    # 4. 保存到数据库
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)

    return db_requirement

@router.get("/", response_model=List[RequirementResponse])
def list_requirements(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "total_score",  # total_score, created_at
    order: str = "desc",  # desc, asc
    db: Session = Depends(get_db)
):
    """获取需求列表，支持排序"""

    query = db.query(Requirement)

    # 排序
    if sort_by == "total_score":
        if order == "desc":
            query = query.order_by(Requirement.total_score.desc())
        else:
            query = query.order_by(Requirement.total_score.asc())
    elif sort_by == "created_at":
        if order == "desc":
            query = query.order_by(Requirement.created_at.desc())
        else:
            query = query.order_by(Requirement.created_at.asc())

    requirements = query.offset(skip).limit(limit).all()
    return requirements

@router.get("/{requirement_id}", response_model=RequirementResponse)
def get_requirement(requirement_id: int, db: Session = Depends(get_db)):
    """获取单个需求详情"""

    requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if not requirement:
        raise HTTPException(status_code=404, detail="需求不存在")

    return requirement

@router.put("/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
    requirement_id: int,
    requirement_update: RequirementUpdate,
    db: Session = Depends(get_db)
):
    """更新需求"""

    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if not db_requirement:
        raise HTTPException(status_code=404, detail="需求不存在")

    # 更新字段
    update_data = requirement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_requirement, field, value)

    # 如果更新了关键字段，重新评估
    key_fields = ["description", "expected_benefit", "affected_user_count",
                  "implementation_cost", "urgency_level", "competitor_info"]
    if any(field in update_data for field in key_fields):
        # 重新评估
        requirement_dict = {
            "title": db_requirement.title,
            "description": db_requirement.description,
            "type": db_requirement.type,
            "business_background": db_requirement.business_background,
            "target_users": db_requirement.target_users,
            "expected_benefit": db_requirement.expected_benefit,
            "affected_user_count": db_requirement.affected_user_count,
            "implementation_cost": db_requirement.implementation_cost,
            "urgency_level": db_requirement.urgency_level,
            "competitor_info": db_requirement.competitor_info,
        }
        evaluation = ai_service.evaluate_requirement(requirement_dict)

        db_requirement.business_value_score = evaluation.business_value_score
        db_requirement.user_impact_score = evaluation.user_impact_score
        db_requirement.cost_score = evaluation.cost_score
        db_requirement.urgency_score = evaluation.urgency_score
        db_requirement.competitor_score = evaluation.competitor_score
        db_requirement.total_score = evaluation.total_score
        db_requirement.ai_recommendation = evaluation.ai_recommendation

    db.commit()
    db.refresh(db_requirement)

    return db_requirement

@router.delete("/{requirement_id}", status_code=204)
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)):
    """删除需求"""

    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if not db_requirement:
        raise HTTPException(status_code=404, detail="需求不存在")

    db.delete(db_requirement)
    db.commit()

    return None
