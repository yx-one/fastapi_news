from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Enum, DateTime, Index, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index("username_UNIQUE", "username", unique=True),
        Index("phone_UNIQUE", "phone", unique=True),
        {"comment": "用户信息表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（加密存储）")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment="头像URL")
    gender: Mapped[str] = mapped_column(Enum("male", "female", "unknown", name="gender_enum"),
                                        server_default="unknown", comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(500), comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                                                 comment="更新时间")

class UserToken(Base):
    __tablename__ = "user_token"
    __table_args__ = (
        Index("token_UNIQUE", "token", unique=True),
        Index("fk_user_token_user_idx", "user_id"),
        {"comment": "用户令牌表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        comment="用户ID",
    )
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )