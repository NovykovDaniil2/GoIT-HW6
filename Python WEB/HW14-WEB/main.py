import redis.asyncio as redis
from fastapi import FastAPI, Depends
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users
from src.conf.config import settings

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    such as database connections or caches.

    :return: A coroutine
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host,
                          port=settings.redis_port, 
                          password=settings.redis_password,
                          db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value
        &quot;Hi! Welcome to the address book!

    :return: A dictionary with a message key
    :doc-author: Trelent
    """
    return {"message": "Hi! Welcome to the address book!"}
