from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.template import Template
from app.models.user import User, UserRole
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.services.auth import get_current_active_user, require_editor_or_above, require_admin

router = APIRouter(prefix="/templates", tags=["需求模版"])


@router.post("/", response_model=TemplateResponse, status_code=201)
def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor_or_above)
):
    """创建需求模版（需要编辑者或管理员权限）"""
    db_template = Template(
        **template.model_dump(),
        created_by=current_user.id
    )

    db.add(db_template)
    db.commit()
    db.refresh(db_template)

    return db_template


@router.get("/", response_model=List[TemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取所有模版列表（所有登录用户可见）"""
    templates = db.query(Template).order_by(Template.is_default.desc(), Template.created_at.desc()).all()
    return templates


@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取单个模版详情"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模版不存在"
        )

    return template


@router.put("/{template_id}", response_model=TemplateResponse)
def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新模版（管理员或创建者）"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模版不存在"
        )

    # 只有管理员或创建者可以修改
    if current_user.role != UserRole.ADMIN and db_template.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限修改此模版"
        )

    update_data = template_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_template, field, value)

    db.commit()
    db.refresh(db_template)

    return db_template


@router.delete("/{template_id}", status_code=204)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """删除模版（仅管理员）"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模版不存在"
        )

    db.delete(db_template)
    db.commit()

    return None
