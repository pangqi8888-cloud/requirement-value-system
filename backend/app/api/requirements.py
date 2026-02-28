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

    # 3. 保存评估结果（新字段）
    db_requirement.universality_score = evaluation.universality_score
    db_requirement.competitor_score = evaluation.competitor_score
    db_requirement.revenue_score = evaluation.revenue_score
    db_requirement.total_score = evaluation.total_score
    db_requirement.ai_recommendation = evaluation.ai_recommendation

    # 兼容旧字段
    db_requirement.business_value_score = evaluation.universality_score
    db_requirement.user_impact_score = evaluation.revenue_score

    # 4. 保存到数据库
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)

    return db_requirement

@router.get("/", response_model=List[RequirementResponse])
def list_requirements(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "total_score",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    """获取需求列表，支持排序"""

    query = db.query(Requirement)

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

    update_data = requirement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_requirement, field, value)

    # 关键字段更新时重新评估
    key_fields = ["description", "expected_benefit", "implementation_cost"]
    if any(field in update_data for field in key_fields):
        requirement_dict = {
            "title": db_requirement.title,
            "description": db_requirement.description,
            "type": db_requirement.type,
            "business_background": db_requirement.business_background,
            "expected_benefit": db_requirement.expected_benefit,
            "implementation_cost": db_requirement.implementation_cost,
        }
        evaluation = ai_service.evaluate_requirement(requirement_dict)

        db_requirement.universality_score = evaluation.universality_score
        db_requirement.competitor_score = evaluation.competitor_score
        db_requirement.revenue_score = evaluation.revenue_score
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
