import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from toutiao_backend.routers import news

app = FastAPI()


# 允许的来源（可以是域名列表）
origins = [
	"http://localhost",
	"http://localhost:3000",
	"https://your-frontend-domain.com"  # 你的前端域名
]

# 添加 CORS中间件
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # 允许访问的源， 开发期间可以写*， 正式写允许的来源
	allow_credentials=True, # 允许携带Cookie
	allow_methods=["*"],   # 允许所有请求方法
	allow_headers=["*"],   # 允许所有请求头
)

app.include_router(news.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)