from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import db_conf
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse
from toutiao_backend.utils.auth import get_current_user
from toutiao_backend.utils.responses import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id: int = Query(default=..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_conf.get_database)
):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckResponse(isFavorite=is_favorited)
    )