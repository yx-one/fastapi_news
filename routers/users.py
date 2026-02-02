from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from toutiao_backend.config import db_conf
from toutiao_backend.crud import users
from toutiao_backend.schemas.user import UserRequest, UserAuthResponse, UserInfoResponse
from toutiao_backend.utils.responses import success_response

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(
    user_data: UserRequest,
    db: AsyncSession = Depends(db_conf.get_database),
):
    # 注册逻辑：验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已存在"
        )

    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(db_conf.get_database)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成token -> 响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功!", data=response_data)
