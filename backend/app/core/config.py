from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "需求价值评估系统"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # 数据库配置（暂时使用内存存储）
    DATABASE_URL: str = "sqlite:///./requirements.db"

    # CORS 配置
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        case_sensitive = True

settings = Settings()
