from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import requirements, auth, users, templates
from app.db.session import engine, Base

# 导入所有模型，确保表被创建
from app.models import requirement, user, template

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["认证"]
)

app.include_router(
    requirements.router,
    prefix=f"{settings.API_V1_STR}/requirements",
    tags=["requirements"]
)

app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["用户管理"]
)

app.include_router(
    templates.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["需求模版"]
)

@app.get("/")
def root():
    return {
        "message": "需求价值评估系统 API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
