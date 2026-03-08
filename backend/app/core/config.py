import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "需求价值评估系统"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./requirements.db")

    # CORS 配置 - 支持本地开发和 Render 部署
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # CORS 正则表达式 - 支持所有 onrender.com 子域名
    BACKEND_CORS_ORIGIN_REGEX: str = r"https://.*\.onrender\.com"

    # JWT 密钥配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

    class Config:
        case_sensitive = True

settings = Settings()
