"""
Financial Intelligence System - Backend API
女性起業家向け金融インテリジェンス配信システム
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    logger.info("Starting Financial Intelligence System Backend...")
    # 起動時の初期化処理
    yield
    # シャットダウン時のクリーンアップ処理
    logger.info("Shutting down Financial Intelligence System Backend...")


app = FastAPI(
    title="Financial Intelligence System API",
    description="女性起業家向け金融インテリジェンス配信システム",
    version="1.0.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """ヘルスチェックエンドポイント"""
    return JSONResponse({
        "status": "healthy",
        "service": "Financial Intelligence System",
        "version": "1.0.0"
    })


@app.get("/health")
async def health_check():
    """詳細ヘルスチェック"""
    return JSONResponse({
        "status": "healthy",
        "components": {
            "api": "up",
            "database": "pending",  # TODO: DB接続チェック
            "scraper": "pending",   # TODO: スクレイパーチェック
            "ai_agent": "pending"   # TODO: AIエージェントチェック
        }
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
