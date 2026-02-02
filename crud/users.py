# 根据用户名查询数据库
import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.models.users import User, UserToken
from toutiao_backend.schemas.user import UserRequest
from toutiao_backend.utils import security


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 密码加密并写入数据库
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库中返回最新的 user
    return user



async def create_token(db: AsyncSession, user_id: int):
    # 生成 Token + 设置过期时间
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)

    # 查询当前用户是否已有 Token
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 已存在则更新
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 不存在则创建
        user_token = UserToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        db.add(user_token)

    await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user


# 根据 Token查询用户：验证Token -> 查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()