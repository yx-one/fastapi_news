from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(message: str="success", data=None):
    content = {"code": 200, "message": message, "data": data}

    # 将任意 Python 对象（如 Pydantic 模型、datetime、ORM 对象等）
    # 转换为可被 JSON 序列化的基础类型（dict / list / str / int 等）
    # (把任何FastAPI，Pydantic,ORM对象转换成可以被JSON安全序列化的数据结构)
    return JSONResponse(content=jsonable_encoder(content))