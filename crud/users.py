# 根据用户名查询数据库
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.models.users import User
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


