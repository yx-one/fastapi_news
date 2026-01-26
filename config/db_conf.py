from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

ASYNC_DATABASE_URL = "mysql+aiomysql://root:159874@localhost:3306/news_app?charset=utf8mb4"   # todo: 改密码 和 数据库名字

# 创建异步引擎
async_engine = create_async_engine(
	ASYNC_DATABASE_URL,
	echo=True, # 可选，输出SQL日志
	pool_size=10, # 设置连接池中保持的持久连接数
	max_overflow=20 # 设置连接池允许创建的额外连接数
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
	bind=async_engine, # 绑定数据库引擎
	class_ = AsyncSession, # 指定会话类
	expire_on_commit=False  # 会话对象不过期，不重新查询数据库
)

# 依赖项，用于获取数据库会话
async def get_database():
	async with AsyncSessionLocal() as session:
		try:
			yield session # 返回数据库会话给路由处理函数
			await session.commit() # 无异常，提交事务
		except Exception:
			await session.rollback() # 有异常则回滚
			raise
		finally:
			await session.close() # 关闭会话
