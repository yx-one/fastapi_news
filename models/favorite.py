from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, INTEGER, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from schemas.base import Base

class Favorite(Base):
    """收藏表 ORM 模型"""

    __tablename__ = "favorite"
    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="user_news_unique"),
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
        {"comment": "收藏表"},
    )

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, comment="收藏ID")

    user_id: Mapped[int] = mapped_column(INTEGER, nullable=False, comment="用户ID")

    news_id: Mapped[int] = mapped_column(INTEGER, nullable=False, comment="新闻ID")

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(),
        comment="收藏时间",
    )