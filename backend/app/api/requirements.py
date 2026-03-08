from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from datetime import datetime
from app.db.session import get_db
from app.models.requirement import Requirement
from app.models.user import User, UserRole
from app.schemas.requirement import RequirementCreate, RequirementResponse, RequirementUpdate
from app.services.ai_evaluation import ai_service
from app.services.auth import get_current_active_user, require_editor_or_above

router = APIRouter()

@router.post("/", response_model=RequirementResponse, status_code=201)
def create_requirement(
    requirement: RequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor_or_above)
):
    """创建需求并进行 AI 评估（需要编辑者或管理员权限）"""

    # 1. 创建需求对象
    db_requirement = Requirement(**requirement.model_dump())
    db_requirement.created_by = current_user.id

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取需求列表，支持排序（需要登录）"""

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

@router.get("/export")
def export_requirements(
    format: str = "csv",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """导出需求列表 CSV（需要登录）"""

    # 获取所有需求
    requirements = db.query(Requirement).order_by(Requirement.total_score.desc()).all()

    # 创建 CSV 数据
    output = io.StringIO()
    writer = csv.writer(output)

    # 写入表头
    writer.writerow([
        "ID", "标题", "类型", "状态", "综合得分", "普适性", "竞品对比",
        "收益潜力", "业务背景", "预期收益", "实现成本", "创建时间", "AI建议"
    ])

    # 写入数据
    for req in requirements:
        writer.writerow([
            req.id,
            req.title,
            req.type.value if hasattr(req.type, 'value') else req.type,
            req.status.value if hasattr(req.status, 'value') else req.status,
            round(req.total_score, 2) if req.total_score else 0,
            round(req.universality_score, 2) if req.universality_score else 0,
            round(req.competitor_score, 2) if req.competitor_score else 0,
            round(req.revenue_score, 2) if req.revenue_score else 0,
            req.business_background or "",
            req.expected_benefit or "",
            req.implementation_cost or "",
            req.created_at.strftime("%Y-%m-%d %H:%M:%S") if req.created_at else "",
            (req.ai_recommendation or "")[:500]  # 限制长度
        ])

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"requirements_{timestamp}.csv"

    # 返回 CSV 文件
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv; charset=utf-8-sig"
        }
    )

@router.get("/{requirement_id}", response_model=RequirementResponse)
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取单个需求详情（需要登录）"""

    requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if not requirement:
        raise HTTPException(status_code=404, detail="需求不存在")

    return requirement

@router.put("/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
    requirement_id: int,
    requirement_update: RequirementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor_or_above)
):
    """更新需求（需要编辑者或管理员权限）"""

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
def delete_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor_or_above)
):
    """删除需求（编辑者只能删除自己的，管理员可以删除任何需求）"""

    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if not db_requirement:
        raise HTTPException(status_code=404, detail="需求不存在")

    # 编辑者只能删除自己创建的需求
    if current_user.role == UserRole.EDITOR and db_requirement.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="您只能删除自己创建的需求"
        )

    db.delete(db_requirement)
    db.commit()

    return None

