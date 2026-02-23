from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import db_conf
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
from toutiao_backend.utils.auth import get_current_user
from toutiao_backend.utils.responses import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id:  Annotated[int, Query(..., alias="newsId")],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_conf.get_database)
):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckResponse(isFavorite=is_favorited)
    )

@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_conf.get_database)
):
    print(data.model_dump())
    await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功")

@router.delete("/remove")
async def remove_favorite(
    news_id:  Annotated[int, Query(..., alias="newsId")],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_conf.get_database)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏记录不存在"
        )
    return success_response(message="取消收藏成功")