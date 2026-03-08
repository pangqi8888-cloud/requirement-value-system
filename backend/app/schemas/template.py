from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    fields_config: Dict[str, Any]
    is_default: bool = False


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fields_config: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None


class TemplateResponse(TemplateBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
